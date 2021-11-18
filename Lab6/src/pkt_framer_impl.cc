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
	using namespace std;
//	cout << "forecasting..." << endl;
//	cout << "noutput_items " << noutput_items << endl;
//	cout << "ninput_items_required " << ninput_items_required[0]  << endl;
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

//		cout << "noutput_items = " << noutput_items << endl;
//		cout << "noutput_items/_payload_size = " << i << endl;
		// Adding header

		// Fixed Preamble
        // 0011 0111 1000 1001
        // *out = 0x3789;
//        cout << "Packet: " << i << endl;
//        cout << "Sending Preamble -----" << endl;
        *out = 0x37;
		int b01 = 55;
//		cout << "bits01: " << b01 << endl;
		out++;
		*out = 0x89;
		int b23 = 137;
//		cout << "bits23: " << b23 << endl;
		out++;

		// Flow id (configurable by user)
		*out = _flow_id;
		int b4 = *out;
		out++;

		// Packet Size (configurable by user)
		*out = _payload_size;
		int b5 = *out;
//		cout << "payload: " << b5 << endl;
		out++;

		int sum = 0; // sum of user data
		// User data
//		cout << "Sending User Data -----" << endl;
		for(int i = 0; i < _payload_size; i++,out++,in++)
		{
			*out = *in;
			int data = *in;
			sum = sum + data;
//			cout << "sum: " << sum << endl;

		}

		// Simple 8bit Checksum
		// Modulo 152 is used b/c the max value encoded into char is 152
		int checksum = (b01 + b23 + b4 + b5 + sum) % 152; // calc
		*out = checksum;
		out++;

        //		cout << "checksum: " << checksum << endl;
		consume(0,int(_payload_size));


	}

    // Tell runtime system how many output items we produced.
	noutput_items = (noutput_items/_payload_size)*(_payload_size + 6);
//    if (noutput_items > 10000){
//        exit();
//    }
//	cout << "noutput_items" << noutput_items << endl;
	cout << "Transmit packet complete" << endl;
        return noutput_items;
    }

  } /* namespace demo */
} /* namespace gr */

