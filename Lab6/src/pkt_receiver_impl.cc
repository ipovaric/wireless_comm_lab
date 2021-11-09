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
#include <bitset>

namespace gr {
  namespace L6_receiver {

    pkt_receiver::sptr
    pkt_receiver::make(int payload_size, int flow_id)
    {
      return gnuradio::get_initial_sptr
        (new pkt_receiver_impl(payload_size,flow_id));
    }

    /*
     * The private constructor
     */
    pkt_receiver_impl::pkt_receiver_impl(int payload_size,int flow_id)
      : gr::block("pkt_receiver",
              gr::io_signature::make(1, 1, sizeof(char)),
              gr::io_signature::make(1, 1, sizeof(char)))
    {
      _payload_size = payload_size;
      _flow_id = flow_id;

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
        ninput_items_required[0] = noutput_items*2;
	using namespace std;
	cout << "receive:noutput_items " << noutput_items << endl;
	cout << "receive:ninput_items_required " << ninput_items_required[0]  << endl;
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
	for(int i = 0; i < noutput_items; i++)
	{
	    cout << "Count: " << i << endl;

	    // For each iteration, pick out four 4-bit items to search for preamble
	    std::bitset<8> xA(in[i]);
	    std::bitset<8> xB(in[i+1]);
	    std::bitset<8> xC(in[i+2]);
	    std::bitset<8> xD(in[i+3]);
	    cout << "itemA" << i << ": " << xA << endl;
	    cout << "itemB" << i << ": " << xB << endl;
	    cout << "itemC" << i << ": " << xC << endl;
	    cout << "itemD" << i << ": " << xD << endl;

	    // if the preamble is correct...do stuff
	    if (xA == 0x03 && xB == 0x07 && xC == 0x08 && xD == 0x09){
            cout << "Preamble 0x3789 found...extracting stream." <<  endl;

            // Write preamble to output stream and make variables for checksum
            *out = in[i];
            int b0 = xA.to_ulong();
            out++;
            *out = in[i+1];
            int b1 = xB.to_ulong();
            out++;
            *out = in[i+2];
            int b2 = xC.to_ulong();
            out++;
            *out = in[i+3];
            int b3 = xD.to_ulong();
            out++;

            // merge bytes
            uint8_t b01 = in[i] | in[i+1];
            cout << "bits01: " << b01 << endl;

            // get flow id and payload size from packet
            //  skipping idx 4 and 6 b/c of extra zero items due to encoding of int types
            std::bitset<8> flow_id_bit(in[i+5]);
            int flow_id = flow_id_bit.to_ulong();
            std::bitset<8> payload_bit(in[i+7]);
            int payload = payload_bit.to_ulong();

//            cout << "flow_id_in: " << _flow_id << endl;
//            cout << "flow_id_stream: " << flow_id.to_ulong() << endl;

            // Check that flow id byte matches the input variable
            if (flow_id == _flow_id){
                cout << "Flow ID Matched:" << flow_id << endl;
                cout << "Payload Size: " << payload << endl;

                // write flow id and payload size to output
                *out = in[i+5]; // flow_id
                out++;
                *out = in[i+7]; // payload
                out++;

                // If all matched, write the data
                cout << "Writing Data to Stream..." << endl;
                int offset = 8; // offset due to preamble
                int datasum = 0;
                for(int j=i+offset; j < payload+i+offset; j++,out++){
                    *out = in[j];
                    std::bitset<8> data_bit(in[j]);
                    int data = data_bit.to_ulong();
                    cout << data_bit << ": " << data << endl;

                    // calc sum for checksum
                    datasum += data;
                }

                // compare checksums
                int sum = b0+b1+b2+b3+flow_id+payload+datasum;
                cout << "Calc Sum: " << sum << endl;
                int chk_byte = in[payload+i+offset+1];
                cout << "Sum from pkt: " << chk_byte << endl;
                if (sum == chk_byte){
                    cout << "Checksums Matched!" << endl;
                } else {
                    cout << "Warning: Checksums not Matched!" << endl;
                }

            }

	    }
		consume(0,int(noutput_items));

	}

        // Tell runtime system how many output items we produced.
	cout << "packet processed" << endl;
        return noutput_items;
    }

  } /* namespace demo */
} /* namespace gr */

