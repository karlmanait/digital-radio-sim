import pytest
import numpy
import core.system
import core.radio.tx.transmitter as tx
import core.radio.rx.receiver as rx


SAMPLING_RATE = 1000000
SIM_DURATION = 1.0

testconfig_radio = [
    # modulation, carrier frequency, symbol duration
    ( 'BPSK',  '80', '0.2'),
    ( 'BPSK',  '90', '0.1'),
    ( 'QPSK', '100', '0.2'),
    ( 'QPSK', '110', '0.1'),
    ('16QAM', '120', '0.2'),
    ('16QAM', '130', '0.1'),
    # extreme symbol duration
    ( 'BPSK', '1000', '0.001'),
    ( 'QPSK', '2000', '0.001'),
    ('16QAM', '3000', '0.001'),
    # mismatched frequency and symbol duration
    ( 'BPSK',    '8', '0.200'),
    ( 'BPSK',   '10', '0.250'),
    ( 'QPSK',  '123', '0.120'),
    ('16QAM', '1234', '0.123'),
]

@pytest.fixture(scope='module')
def system():
    system = core.system.System()
    system.config_update(
        system=
        {
            'sampling rate': str(SAMPLING_RATE),
            'sim duration' : str(SIM_DURATION)
        }
    )
    return system

def update_system_config(system, configs):
    system.config_update(
        tx1=
        {
            'modulation': configs[0],
            'carrier frequency': configs[1],
            'symbol duration': configs[2],
        },
        rx1=
        {
            'modulation': configs[0],
            'carrier frequency': configs[1],
            'symbol duration': configs[2],
        }
    )
    length = int(SIM_DURATION/float(configs[2]))
    if 'BPSK' == configs[0]:
        multiple = 1
    elif 'QPSK' == configs[0]:
        multiple = 2
    elif '16QAM' == configs[0]:
        multiple = 4
    return (length*multiple, multiple)

@pytest.mark.parametrize('configs', testconfig_radio)
def test_full_duration(system, configs):
    tx1 = tx.Transmitter(system, 'tx1')
    rx1 = rx.Receiver(system, 'rx1')
    system.radio_add(rx1)
    system.radio_add(tx1)
    bitstream_size = update_system_config(system, configs)[0]
    tx1.bitstream = numpy.random.randint(low=0, high=2, size=bitstream_size, dtype=numpy.int8)
    system.run()
    assert (tx1.bitstream == rx1.bitstream).all()

@pytest.mark.parametrize('configs', testconfig_radio)
def test_partial_duration(system, configs):
    tx1 = tx.Transmitter(system, 'tx1')
    rx1 = rx.Receiver(system, 'rx1')
    system.radio_add(rx1)
    system.radio_add(tx1)
    length = update_system_config(system, configs)
    bitstream_size = numpy.random.randint(low=length[1], high=length[0]-length[1])
    tx1.bitstream = numpy.random.randint(low=0, high=2, size=bitstream_size, dtype=numpy.int8)
    system.run()
    assert (tx1.bitstream == rx1.bitstream).all()

@pytest.mark.parametrize('configs', testconfig_radio)
def test_exceed_duration(system, configs):
    tx1 = tx.Transmitter(system, 'tx1')
    rx1 = rx.Receiver(system, 'rx1')
    system.radio_add(rx1)
    system.radio_add(tx1)
    length = update_system_config(system, configs)
    bitstream_size = numpy.random.randint(low=length[0]+length[1], high=2*length[0])
    tx1.bitstream = numpy.random.randint(low=0, high=2, size=bitstream_size, dtype=numpy.int8)
    system.run()
    assert (tx1.bitstream[:length[0]] == rx1.bitstream).all()