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
        ninput_items_required[0] = noutput_items;
	using namespace std;
//	cout << "receive:noutput_items " << noutput_items << endl;
//	cout << "receive:ninput_items_required " << ninput_items_required[0]  << endl;
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

    // Main signal processing
    int pkt_cnt = 0; // packet counter
    cout << "Searching Index..." << endl;
	for(int i = 0; i < noutput_items; i++)
	{
        using namespace std;

        vector<string> pream_chk (4); // preamble checker container
        vector<string> pream_valid {"0011","0111","1000","1001"}; // valid preamble
        bool flow_id_valid;
        bool valid_stream = false; // will be true if preamble is found

        // Extract four bytes of data to look for preamble
        for(int j = 0; j < 4; j++){
            int x0(*in); in++;
            int x1(*in); in++;
            int x2(*in); in++;
            int x3(*in); in++;
            pream_chk[j] = to_string(x0)+to_string(x1)+to_string(x2)+to_string(x3);
        }

        int fid_num;
	    if (pream_chk == pream_valid){
            cout << endl;
            cout << "***************************" << endl;
            cout << "Index: " << i << endl;
            cout << "Preamble Matched!! <<<<---" << endl;
            cout << "***************************" << endl;

            // extract flow_id
            in = in + 4; // skip blank bytes
            int x0(*in); in++;
            int x1(*in); in++;
            int x2(*in); in++;
            int x3(*in); in++;
            bitset<4> fid_data(to_string(x0)+to_string(x1)+to_string(x2)+to_string(x3));
            fid_num = fid_data.to_ulong();
            cout << "Flow ID: " << fid_num << " ";

            // compare flow id and output if correct
            if(fid_num==_flow_id){
                cout << "Flow ID Matched!" << endl;

                // output preamble bytes
                *out = 0x37;
                out++;
                *out = 0x89;
                out++;

                // output flow id bytes
//                *out = 0x00; // blank byte
//                out++;
                *out = fid_num;
                out++;

                pkt_cnt++; // increment packet count
                valid_stream = true; // only true if both preamble and flow id are matched

            }

        } else {
            in = in - 15; // go back to just after the first index
        }

        // if the preamble is found and flow id is matched, do this stuff
        if(valid_stream) {
            // extract payload_size
            in = in + 4; // skip blank bytes
            int x0(*in); in++;
            int x1(*in); in++;
            int x2(*in); in++;
            int x3(*in); in++;
            bitset<4> pyld_data(to_string(x0)+to_string(x1)+to_string(x2)+to_string(x3));

            // output payload_size
            *out = pyld_data.to_ulong();
            out++;

            // extract and output user data (8 bits)*payload_size
            int user_sum = 0;
            for (int j = 0; j < _payload_size; j++){
                int x0(*in); in++;
                int x1(*in); in++;
                int x2(*in); in++;
                int x3(*in); in++;
                int x4(*in); in++;
                int x5(*in); in++;
                int x6(*in); in++;
                int x7(*in); in++;
                bitset<8> user_data(to_string(x0)+to_string(x1)+to_string(x2)+to_string(x3)+to_string(x4)+to_string(x5)+to_string(x6)+to_string(x7));

                *out = user_data.to_ulong();
                out++;

                cout << "User Data" << j << ": " << user_data.to_ulong() << endl;

                user_sum = user_sum + user_data.to_ulong(); // for checksum
            }

            // extract checksum data (8bits)
            int x4(*in); in++;
            int x5(*in); in++;
            int x6(*in); in++;
            int x7(*in); in++;
            int x8(*in); in++;
            int x9(*in); in++;
            int x10(*in); in++;
            int x11(*in); in++;
            bitset<8> chksum_data(to_string(x4)+to_string(x5)+to_string(x6)+to_string(x7)+to_string(x8)+to_string(x9)+to_string(x10)+to_string(x11));
            cout << "checksum_data: " << chksum_data.to_ulong() << endl;

            // checksum calculation
            // preamble+flow_id+payload_size+user_data
            int chksum_calc = (192 + fid_num + pyld_data.to_ulong() + user_sum) % 152;
            cout << "checksum_calc: " << chksum_calc << endl;
            if(chksum_data == chksum_calc){
                cout << "Checksums Matched!!" << endl;
            } else {
                cout << "Warning: Checksums NOT Matched!!" << endl;
            }

            *out = chksum_calc;
            out++;

            // Break included to stop reading when zero data is read
            if(user_sum == 0 && valid_stream){
                break;
            }

        // Break included to keep output from running away and getting stuck
        if(i > 1000){
            break;
        }
        }
		consume(0,int(noutput_items));

	}

        // Tell runtime system how many output items we produced.
	cout << endl << "Total of " << pkt_cnt << " Packets Processed." << endl;
        return noutput_items;
    }

  } /* namespace demo */
} /* namespace gr */

