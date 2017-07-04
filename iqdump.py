#! /usr/bin/env python

import argparse
import json

from rx_block import rx_block

def parse_args():
    # Hardcoded default settings for GNURadio
    settings = {
            'center_freq' : 443000000,
            'sample_rate' : 5000000,
            'device_string' : '',
            'iq_file' : ''}

    parser = argparse.ArgumentParser('Dump or replay raw SDR IQ samples.')
    parser.add_argument('-r', '--replay', action='store_true', 
            help='Replay mode.')
    parser.add_argument('-f', '--frequency', help='Specify center frequency.')
    parser.add_argument('-s', '--sample-rate', help='Specify sample rate.')
    parser.add_argument('-m', '--metadata', action='store_true', 
        help='Store metadata in '
        'FILE, and IQ data in FILE.dat. When replaying, load metadata '
        'from FILE, and use IQ data as specified in the metadata file. The '
        '-F/--data-file option modifies this behavior. Additionally, any '
        'other options specified during replay will override those saved '
        'in the metadata file')
    parser.add_argument('-F', '--data-file', action='store', 
        help='When dumping with the -m '
        'option, specifies the filename to store IQ data, rather than '
        'FILE.dat. When replaying, override the referenced data in '
        'the metadata file with the specified file.')
    parser.add_argument('-d', '--device-string', help='OsmoSDR Device String.')
    parser.add_argument('file')

    # Parse command-line args
    args = parser.parse_args()

    # Determine mode
    replay = args.replay
    metadata = args.metadata

    # If replaying in metadata mode, load metadata
    if metadata and replay:
        with open(args.file, 'r') as mdfile:
            md = json.loads(mdfile.read())
            if md['center_freq']:
                settings['center_freq'] = md['center_freq']
            if md['sample_rate']:
                settings['sample_rate'] = md['sample_rate']
            if md['device_string']:
                settings['device_string'] = md['device_string']
            if md['iq_file']:
                settings['iq_file'] = md['iq_file']
    elif metadata:
        # Metadata dump, construct filename (overridden by -F if applicable)
        settings['iq_file'] = args.file + '.dat'

    # Set/override based on command line
    if args.frequency:
        settings['center_freq'] = int(args.frequency)
    if args.sample_rate:
        settings['sample_rate'] = int(args.sample_rate)
    if args.device_string:
        settings['device_string'] = args.device_string

    # If not operating in metadata mode, iq_file is FILE
    if not metadata:
        settings['iq_file'] = args.file

    # If in metadata mode and -F is specified, use that
    if metadata and args.data_file:
        settings['iq_file'] = args.data_file

    # Save metadata file if dumping in metadata mode
    if metadata and not replay:
        with open(args.file, 'w') as mdfile:
            mdfile.write(json.dumps(settings, indent=4, separators=(',', ': ')))
    
    # Return settings and mode
    return settings, replay

def print_settings(settings, replay):
    if replay:
        print("Replaying IQ data...")
    else:
        print("Dumping IQ data...")

    print("    IQ file           : " + settings['iq_file'])
    print("    Center frequency  : " + str(settings['center_freq']))
    print("    Sample rate       : " + str(settings['sample_rate']))
    print("    Device string     : " + settings['device_string'])

if __name__ == '__main__':
    settings, replay = parse_args()
    print_settings(settings, replay)

    if replay:
        tb = tx_block(settings)
    else:
        tb = rx_block(settings)

    tb.start()
    raw_input('Press Enter to quit: ')
    tb.stop()
    tb.wait()

