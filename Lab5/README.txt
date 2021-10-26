Command Line Arguments used for trials:


While in ns directory:

edit the file:
pico scratch/wifi-simple-adhoc-grid.cc

Run the simulation:
./waf
./waf --run "wifi-simple-adhoc-grid.cc --numPackets=<int> --interval=<float>"

Evaluate results:
python3 ~/repos/wireless_comm_lab/Lab5/flowmon-parse-results_Lab5.py wifi-simple-adhoc-grid.xml

  Ptr<Socket> recvSink2 = Socket::CreateSocket (c.Get (sinkNode2), tid); // 2nd flow
  InetSocketAddress local2 = InetSocketAddress (Ipv4Address::GetAny (), 81);
  recvSink2->Bind (local2);
  recvSink2->SetRecvCallback (MakeCallback (&ReceivePacket));

  Ptr<Socket> source2 = Socket::CreateSocket (c.Get (sourceNode2), tid);
  InetSocketAddress remote2 = InetSocketAddress (i.GetAddress (sinkNode2, 0), 81);
  source2->Connect (remote2);

  Simulator::Schedule (Seconds (29.9), &GenerateTraffic,
                       source2, packetSize, numPackets, interPacketInterval);