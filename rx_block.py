from gnuradio import gr
from gnuradio import blocks

import osmosdr

class rx_block(gr.top_block):
    def __init__(self, settings):
        gr.top_block.__init__(self, "IQDump Receive Block")

        # Save settings
        self.samp_rate = settings['sample_rate']
        self.center_freq = settings['center_freq']
        self.device_string = settings['device_string']
        self.iq_file = settings['iq_file']

        # Blocks
        self.osmosdr_source_0 = osmosdr.source(args='numchan=1 ' +
                self.device_string)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.osmosdr_source_0.set_center_freq(self.center_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)

        self.file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, 
                self.iq_file, True)
        self.file_sink_0.set_unbuffered(False)

        # Connections
        self.connect((self.osmosdr_source_0, 0),
                (self.file_sink_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
