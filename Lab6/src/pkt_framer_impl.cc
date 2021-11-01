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
#include "pkt_framer_impl.h"
#include <iostream>

namespace gr {
  namespace demo {

    pkt_framer::sptr
    pkt_framer::make(int payload_size, int flow_id)
    {
      return gnuradio::get_initial_sptr
        (new pkt_framer_impl(payload_size,flow_id));
    }

    /*
     * The private constructor
     */
    pkt_framer_impl::pkt_framer_impl(int payload_size,int flow_id)
      : gr::block("pkt_framer",
              gr::io_signature::make(1, 1, sizeof(char)),
              gr::io_signature::make(1, 1, sizeof(char)))
    {
      _payload_size = payload_size;
      _flow_id = flow_id;

    }

    /*
     * Our virtual destructor.
     */
    pkt_framer_impl::~pkt_framer_impl()
    {
    }

    void
    pkt_framer_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
	// payload + 6 bytes header = output
        ninput_items_required[0] = (noutput_items/_payload_size+1)*(_payload_size - 6);
	//using namespace std;
	std::cout << "noutput_items " << noutput_items << std::endl;
	std::cout << "ninput_items_required " << ninput_items_required[0]  << std::endl;
    }

    int
    pkt_framer_impl::general_work (int noutput_items,
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
	for(int i = noutput_items/_payload_size; i > 0; i--)
	{
		//cout << "noutput_items = " << noutput_items << endl;
		//cout << "payload_size = " << _payload_size << endl;
		//cout << "noutput_items/_payload_size = " << i << endl;
		// Adding header

		// Preamble
		*out = 0x37;
		int b01 = *out;
		out++;
//		*out = 0x07;
//		int b1 = *out;
//		out++;

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
		/*
		cout << "Byte0= " << b0 << endl;
		cout << "Byte1= " << b1 << endl;
		cout << "Byte2= " << b2 << endl;
		cout << "Byte3= " << b3 << endl;
		cout << "UserDataSize= " << sz << endl;
		*/

		// CRC Checksum
		int checksum = b01 + b2 + b3 + sz;
		*out = checksum;
		//cout << "checksum= " << checksum << endl;
		out++;

		// sheild bit
		*out = 0x00;
		out++;

		consume(0,int(_payload_size));

	}

        // Tell runtime system how many output items we produced.
	noutput_items = (noutput_items/_payload_size)*(_payload_size + 6);
	cout << "noutput_items" << noutput_items << endl;
	cout << "packet complete" << endl;
        return noutput_items;
    }

  } /* namespace demo */
} /* namespace gr */

