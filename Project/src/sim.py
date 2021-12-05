#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Sim
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

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.fft import window
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from wifi_phy_hier import wifi_phy_hier  # grc-generated hier_block
import foo
import pmt
import ieee802_11
import math
import random



from gnuradio import qtgui

class sim(gr.top_block, Qt.QWidget):

    def __init__(self, encoding=1, messages=1000, pdu_len=133, repetition=23, snr=10):
        gr.top_block.__init__(self, "Sim", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Sim")
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

        self.settings = Qt.QSettings("GNU Radio", "sim")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.encoding = encoding
        self.messages = messages
        self.pdu_len = pdu_len
        self.repetition = repetition
        self.snr = snr

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.out_buf_size = out_buf_size = 96000
        self.filename = filename =  "results/sim_%d_%d_%.1f_.pcap" % (repetition, encoding, snr)

        ##################################################
        # Blocks
        ##################################################
        self.wifi_phy_hier_0 = wifi_phy_hier(
            bandwidth=10e6,
            chan_est=ieee802_11.LS,
            encoding=encoding,
            frequency=5.89e9,
            sensitivity=0.56,
        )
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.ieee802_11_mac_0 = ieee802_11.mac([0x23, 0x23, 0x23, 0x23, 0x23, 0x23], [0x42, 0x42, 0x42, 0x42, 0x42, 0x42], [0xff, 0xff, 0xff, 0xff, 0xff, 0xff])
        self.foo_wireshark_connector_0 = foo.wireshark_connector(127, False)
        self.foo_random_periodic_msg_source_0 = foo.random_periodic_msg_source(pdu_len - 24, 5, messages, False, False, repetition)
        self.foo_packet_pad2_0 = foo.packet_pad2(False, False, 0.001, 1000, 1000)
        self.foo_packet_pad2_0.set_min_output_buffer(96000)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc((10**(snr/10.0))**.5)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_char*1, filename, False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 1, repetition)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.foo_random_periodic_msg_source_0, 'out'), (self.ieee802_11_mac_0, 'app in'))
        self.msg_connect((self.ieee802_11_mac_0, 'phy out'), (self.wifi_phy_hier_0, 'mac_in'))
        self.msg_connect((self.wifi_phy_hier_0, 'mac_out'), (self.foo_wireshark_connector_0, 'in'))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.wifi_phy_hier_0, 0))
        self.connect((self.foo_packet_pad2_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.foo_wireshark_connector_0, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.wifi_phy_hier_0, 0), (self.foo_packet_pad2_0, 0))
        self.connect((self.wifi_phy_hier_0, 0), (self.qtgui_time_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "sim")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_encoding(self):
        return self.encoding

    def set_encoding(self, encoding):
        self.encoding = encoding
        self.set_filename( "results/sim_%d_%d_%.1f_.pcap" % (self.repetition, self.encoding, self.snr))
        self.wifi_phy_hier_0.set_encoding(self.encoding)

    def get_messages(self):
        return self.messages

    def set_messages(self, messages):
        self.messages = messages

    def get_pdu_len(self):
        return self.pdu_len

    def set_pdu_len(self, pdu_len):
        self.pdu_len = pdu_len

    def get_repetition(self):
        return self.repetition

    def set_repetition(self, repetition):
        self.repetition = repetition
        self.set_filename( "results/sim_%d_%d_%.1f_.pcap" % (self.repetition, self.encoding, self.snr))

    def get_snr(self):
        return self.snr

    def set_snr(self, snr):
        self.snr = snr
        self.set_filename( "results/sim_%d_%d_%.1f_.pcap" % (self.repetition, self.encoding, self.snr))
        self.blocks_multiply_const_vxx_0.set_k((10**(self.snr/10.0))**.5)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_out_buf_size(self):
        return self.out_buf_size

    def set_out_buf_size(self, out_buf_size):
        self.out_buf_size = out_buf_size

    def get_filename(self):
        return self.filename

    def set_filename(self, filename):
        self.filename = filename
        self.blocks_file_sink_0_0.open(self.filename)



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-e", "--encoding", dest="encoding", type=intx, default=1,
        help="Set encoding [default=%(default)r]")
    parser.add_argument(
        "-n", "--messages", dest="messages", type=intx, default=1000,
        help="Set messages [default=%(default)r]")
    parser.add_argument(
        "-l", "--pdu-len", dest="pdu_len", type=intx, default=133,
        help="Set pdu_len [default=%(default)r]")
    parser.add_argument(
        "-r", "--repetition", dest="repetition", type=intx, default=23,
        help="Set repetition [default=%(default)r]")
    parser.add_argument(
        "-s", "--snr", dest="snr", type=eng_float, default=eng_notation.num_to_str(float(10)),
        help="Set snr [default=%(default)r]")
    return parser


def main(top_block_cls=sim, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(encoding=options.encoding, messages=options.messages, pdu_len=options.pdu_len, repetition=options.repetition, snr=options.snr)

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
