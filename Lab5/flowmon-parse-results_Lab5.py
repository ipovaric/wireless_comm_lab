from __future__ import division
import sys
import os
try:
    from xml.etree import cElementTree as ElementTree
except ImportError:
    from xml.etree import ElementTree
 
def parse_time_ns(tm):
    if tm.endswith('ns'):
        return float(tm[:-2])
    raise ValueError(tm)
 
 
 
 
class FiveTuple(object):
    
    __slots_ = ['sourceAddress', 'destinationAddress', 'protocol', 'sourcePort', 'destinationPort']
    def __init__(self, el):
        '''! The initializer.
        @param self The object pointer.
        @param el The element.
        '''
        self.sourceAddress = el.get('sourceAddress')
        self.destinationAddress = el.get('destinationAddress')
        self.sourcePort = int(el.get('sourcePort'))
        self.destinationPort = int(el.get('destinationPort'))
        self.protocol = int(el.get('protocol'))
        
 
class Histogram(object):
    
    __slots_ = 'bins', 'nbins', 'number_of_flows'
    def __init__(self, el=None):
        '''! The initializer.
        @param self The object pointer.
        @param el The element.
        '''
        self.bins = []
        if el is not None:
            #self.nbins = int(el.get('nBins'))
            for bin in el.findall('bin'):
                self.bins.append( (float(bin.get("start")), float(bin.get("width")), int(bin.get("count"))) )
 
 
class Flow(object):
    
    __slots_ = ['flowId', 'delayMean', 'packetLossRatio', 'rxBitrate', 'txBitrate',
                'fiveTuple', 'packetSizeMean', 'probe_stats_unsorted',
                'hopCount', 'flowInterruptionsHistogram', 'rx_duration']
    def __init__(self, flow_el):
        '''! The initializer.
        @param self The object pointer.
        @param flow_el The element.
        '''
        self.flowId = int(flow_el.get('flowId'))
        rxPackets = float(flow_el.get('rxPackets'))
        txPackets = float(flow_el.get('txPackets'))
        
        
        # my added variables
        self.timeFirstTxPacket = float(parse_time_ns(flow_el.get('timeFirstTxPacket')))
        self.timeLastTxPacket = float(parse_time_ns(flow_el.get('timeLastTxPacket')))
        self.timeFirstRxPacket = float(parse_time_ns(flow_el.get('timeFirstRxPacket')))
        self.timeLastRxPacket = float(parse_time_ns(flow_el.get('timeLastRxPacket')))
        self.txBytes = float(flow_el.get('txBytes'))
        self.txPackets = float(flow_el.get('txPackets')) # also member above
        self.rxBytes = float(flow_el.get('rxBytes'))
        self.rxPackets = float(flow_el.get('rxPackets')) # also member above
        self.lostPackets = float(flow_el.get('lostPackets'))
        self.timesForwarded = float(flow_el.get('timesForwarded'))
        
 
        tx_duration = (parse_time_ns (flow_el.get('timeLastTxPacket')) - parse_time_ns(flow_el.get('timeFirstTxPacket')))*1e-9
        rx_duration = (parse_time_ns (flow_el.get('timeLastRxPacket')) - parse_time_ns(flow_el.get('timeFirstRxPacket')))*1e-9
        self.rx_duration = rx_duration
        self.probe_stats_unsorted = []
        if rxPackets:
            self.hopCount = float(flow_el.get('timesForwarded')) / rxPackets + 1
        else:
            self.hopCount = -1000
        if rxPackets:
            self.delayMean = float(flow_el.get('delaySum')[:-2]) / rxPackets * 1e-9
            self.packetSizeMean = float(flow_el.get('rxBytes')) / rxPackets
        else:
            self.delayMean = None
            self.packetSizeMean = None
        if rx_duration > 0:
            self.rxBitrate = float(flow_el.get('rxBytes'))*8 / rx_duration
        else:
            self.rxBitrate = None
        if tx_duration > 0:
            self.txBitrate = float(flow_el.get('txBytes'))*8 / tx_duration
        else:
            self.txBitrate = None
        lost = float(flow_el.get('lostPackets'))
        #print "rxBytes: %s; txPackets: %s; rxPackets: %s; lostPackets: %s" % (flow_el.get('rxBytes'), txPackets, rxPackets, lost)
        if rxPackets == 0:
            self.packetLossRatio = None
        else:
            self.packetLossRatio = (lost / (rxPackets + lost))
 
        interrupt_hist_elem = flow_el.find("flowInterruptionsHistogram")
        if interrupt_hist_elem is None:
            self.flowInterruptionsHistogram = None
        else:
            self.flowInterruptionsHistogram = Histogram(interrupt_hist_elem)
 
 
class ProbeFlowStats(object):
    
    __slots_ = ['probeId', 'packets', 'bytes', 'delayFromFirstProbe']
 
 
class Simulation(object):
    
    def __init__(self, simulation_el):
        '''! The initializer.
        @param self The object pointer.
        @param simulation_el The element.
        '''
        self.flows = []
        FlowClassifier_el, = simulation_el.findall("Ipv4FlowClassifier")
        flow_map = {}
        for flow_el in simulation_el.findall("FlowStats/Flow"):
            flow = Flow(flow_el)
            flow_map[flow.flowId] = flow
            self.flows.append(flow)
        for flow_cls in FlowClassifier_el.findall("Flow"):
            flowId = int(flow_cls.get('flowId'))
            flow_map[flowId].fiveTuple = FiveTuple(flow_cls)
 
        for probe_elem in simulation_el.findall("FlowProbes/FlowProbe"):
            probeId = int(probe_elem.get('index'))
            for stats in probe_elem.findall("FlowStats"):
                flowId = int(stats.get('flowId'))
                s = ProbeFlowStats()
                s.packets = int(stats.get('packets'))
                s.bytes = float(stats.get('bytes'))
                s.probeId = probeId
                if s.packets > 0:
                    s.delayFromFirstProbe =  parse_time_ns(stats.get('delayFromFirstProbeSum')) / float(s.packets)
                else:
                    s.delayFromFirstProbe = 0
                flow_map[flowId].probe_stats_unsorted.append(s)
 
 
def main(argv):
    
    file_obj = open(argv[1])
    print("Reading XML file \n")#, end=" ")
 
    sys.stdout.flush()        
    level = 0
    sim_list = []
    for event, elem in ElementTree.iterparse(file_obj, events=("start", "end")):
        if event == "start":
            level += 1
        if event == "end":
            level -= 1
            if level == 0 and elem.tag == 'FlowMonitor':
                sim = Simulation(elem)
                sim_list.append(sim)
                elem.clear() # won't need this any more
                sys.stdout.write(".")
                sys.stdout.flush()
    print(" done.")
    
    # default parameters to add
    # timeFirstTxPacket, timeLastTxPacket, timeFirstRxPacket, timeLastRxPacket
    #   txBytes, txPackets, rxBytes, rxPackets, lostPackets, timesForwarded
    
    # derived parameters to add
    # txBitrate, rxBitrate, delayMean, packetLossRatio, tx_duration, rx_duration,
    #   hopCount, packetSizeMean
 
    idx = ("timeFirstTxPacket timeLastTxPacket timeFirstRxPacket timeLastRxPacket "
        "txBytes txPackets rxBytes rxPackets lostPackets timesForwarded").split()
    for sim in sim_list:
        for flow in sim.flows:
            t = flow.fiveTuple
            proto = {6: 'TCP', 17: 'UDP'} [t.protocol]
            print("FlowID: %i (%s %s/%s --> %s/%i)" % \
                (flow.flowId, proto, t.sourceAddress, t.sourcePort, t.destinationAddress, t.destinationPort))
            if flow.txBitrate is None:
                print("\tTX bitrate: None")
            else:
                print("\tTX bitrate: %.2f kbit/s" % (flow.txBitrate*1e-3,))
            if flow.rxBitrate is None:
                print("\tRX bitrate: None")
            else:
                print("\tRX bitrate: %.2f kbit/s" % (flow.rxBitrate*1e-3,))
            if flow.delayMean is None:
                print("\tMean Delay: None")
            else:
                print("\tMean Delay: %.2f ms" % (flow.delayMean*1e3,))
            if flow.packetLossRatio is None:
                print("\tPacket Loss Ratio: None")
            else:
                print("\tPacket Loss Ratio: %.2f %%" % (flow.packetLossRatio*100))
            print("\tHop Count: %.0f" % (flow.hopCount))
            
            print()
            print("Default Parameters----")
            timeFirstTxPacket = flow.timeFirstTxPacket * 1e-9
            print(f'timeFirstTxPacket: {timeFirstTxPacket:.2f}')
            timeLastTxPacket = flow.timeLastTxPacket * 1e-9
            print(f"timeLastTxPacket: {timeLastTxPacket:.2f} s")
            timeFirstRxPacket = flow.timeFirstRxPacket * 1e-9
            print(f"timeFirstRxPacket: {timeFirstRxPacket:.2f} s")
            timeLastRxPacket = flow.timeLastRxPacket * 1e-9
            print(f"timeLastRxPacket: {timeLastRxPacket:.2f} s")
            print(f"txBytes: {flow.txBytes}")
            print(f"txPackets: {flow.txPackets:.0f}")
            print(f"rxBytes: {flow.rxBytes}")
            print(f"rxPackets: {flow.rxPackets:.0f}")
            print(f"lostPackets: {flow.lostPackets:.0f}")
            print(f"timesForwarded: {flow.timesForwarded:.0f}")
            
    
if __name__ == '__main__':
    main(sys.argv)
