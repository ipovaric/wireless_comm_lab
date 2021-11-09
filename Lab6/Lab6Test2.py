#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Lab6Test3
# GNU Radio version: v3.10.0.0git-520-g4d0f2900

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from gnuradio import blocks
import numpy
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import L6_receiver
import demo



from gnuradio import qtgui

class Lab6Test2(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Lab6Test3", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Lab6Test3")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "Lab6Test2")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 10
        self.payload_size = payload_size = 10
        self.packing = packing = 2
        self.flow_id = flow_id = 1

        ##################################################
        # Blocks
        ##################################################
        self.demo_pkt_framer_0 = demo.pkt_framer(payload_size, flow_id)
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(4, gr.GR_MSB_FIRST)
        self.blocks_head_0 = blocks.head(gr.sizeof_char*1, samp_rate*10)
        self.blocks_file_sink_1_0_1_0 = blocks.file_sink(gr.sizeof_char*1, 'received_after.txt', False)
        self.blocks_file_sink_1_0_1_0.set_unbuffered(False)
        self.blocks_file_sink_1_0_1 = blocks.file_sink(gr.sizeof_char*1, 'received_unpkt.txt', False)
        self.blocks_file_sink_1_0_1.set_unbuffered(False)
        self.blocks_file_sink_1_0_0 = blocks.file_sink(gr.sizeof_char*1, 'received.txt', False)
        self.blocks_file_sink_1_0_0.set_unbuffered(False)
        self.analog_random_source_x_0_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(20, 22, 10))), False)
        self.L6_receiver_pkt_receiver_0 = L6_receiver.pkt_receiver(payload_size, flow_id)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.L6_receiver_pkt_receiver_0, 0), (self.blocks_file_sink_1_0_1_0, 0))
        self.connect((self.analog_random_source_x_0_0, 0), (self.demo_pkt_framer_0, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_file_sink_1_0_0, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.L6_receiver_pkt_receiver_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.blocks_file_sink_1_0_1, 0))
        self.connect((self.demo_pkt_framer_0, 0), (self.blocks_head_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Lab6Test2")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_head_0.set_length(self.samp_rate*10)

    def get_payload_size(self):
        return self.payload_size

    def set_payload_size(self, payload_size):
        self.payload_size = payload_size

    def get_packing(self):
        return self.packing

    def set_packing(self, packing):
        self.packing = packing

    def get_flow_id(self):
        return self.flow_id

    def set_flow_id(self, flow_id):
        self.flow_id = flow_id




def main(top_block_cls=Lab6Test2, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
