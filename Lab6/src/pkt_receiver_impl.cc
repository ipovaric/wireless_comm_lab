/* -*- c++ -*- */
/*
 * Copyright 2014 <+YOU OR YOUR COMPANY+>.
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif


#include <gnuradio/io_signature.h>
#include "pkt_receiver_impl.h"
#include <iostream>

namespace gr {
  namespace demo {

    pkt_receiver::sptr
    pkt_receiver::make()
    {
      return gnuradio::get_initial_sptr
        (new pkt_receiver_impl());
    }

    /*
     * The private constructor
     */
    pkt_receiver_impl::pkt_receiver_impl()
      : gr::block("pkt_receiver",
              gr::io_signature::make(1, 1, sizeof(char)),
              gr::io_signature::make(1, 1, sizeof(char)))
    {
    }

    /*
     * Our virtual destructor.
     */
    pkt_receiver_impl::~pkt_receiver_impl()
    {
    }

    void
    pkt_receiver_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
	// payload + 6 bytes header = output
        ninput_items_required[0] = noutput_items;
	//using namespace std;
	std::cout << "ninput_items_required " << ninput_items_required[0]  << std::endl;
    }

    int
    pkt_receiver_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
	using namespace std;
        const char *in = (const char *) input_items[0];
        char *out = (char *) output_items[0];

        // Do <+signal processing+>
        // Tell runtime system how many input items we consumed on
        // each input stream.
        cout << "rec:noutput_items = " << noutput_items << endl;
	for(int i = 0; i < noutput_items; i++)
	{
		cout << "item" << i << ": " << in[i] << endl;
		// Adding header

		/*if in[i] =
		// Preamble
		*out = 0x03;
		int b0 = *out;
		out++;
		*out = 0x07;
		int b1 = *out;
		out++;

		// Flow id (configurable by user)
		*out = _flow_id;
		int b2 = *out;
		out++;

		// Packet Size (configurable by user)
		*out = _payload_size;
		int b3 = *out;
		out++;

		int sz = 0; // size of user data
		// User data
		for(int i = 0; i < _payload_size; i++,out++,in++)
		{
			*out = *in;
			sz += int(*out);
		}
		cout << "Byte0= " << b0 << endl;
		cout << "Byte1= " << b1 << endl;
		cout << "Byte2= " << b2 << endl;
		cout << "Byte3= " << b3 << endl;
		cout << "UserDataSize= " << sz << endl;

		// CRC Checksum
		int checksum = b0 + b1 + b2 + b3 + sz;
		*out = checksum;
		cout << "checksum= " << checksum << endl;
		out++;

		// sheild bit
		*out = 0x00;
		out++;*/

		consume_each(noutput_items);

	}

        // Tell runtime system how many output items we produced.
	cout << "rec:packet complete" << endl;
        return noutput_items;
    }

  } /* namespace demo */
} /* namespace gr */

