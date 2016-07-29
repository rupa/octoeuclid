import time

from rtmidi.midiutil import open_midiport


rot_knobs = [16, 17, 18, 19, 20, 21, 22, 23]
rst_knobs = [24, 25, 26, 27, 28, 29, 30, 31]
step_pads = [44, 45, 46, 47, 48, 49, 50, 51]
gate_pads = [36, 37, 38, 39, 40, 41, 42, 43]

GATE_HIGH = 127
GATE_LOW = 0


class OctoEuclid(object):
    """
    Up to 8 euclids at once!
    """
    def __init__(self, euclids):
        if len(euclids) > 8:
            raise ValueError('max 8')
        self.slots = euclids

    def reset(self, slot_idx):
        try:
            self.slots[slot_idx].reset()
        except IndexError:
            pass

    def rotate(self, slot_idx):
        try:
            self.slots[slot_idx].rotate()
        except IndexError:
            pass

    def step(self):
        return [x.step() for x in self.slots]

    def __len__(self):
        return len(self.slots)

    def __str__(self):
        details = '\n'.join(str(x) for x in self.slots)
        return 'OctoEuclid({0}):\n{1}'.format(len(self.slots), details)


class BeatStepPro(object):
    """
    """

    def __init__(self, octoeuclid=None, gate_len=0.01):
        """
        """
        self.midiin, self.port_in_name = open_midiport(
            -1,
            'input',
            client_name='euclid',
            port_name='euclid input_port'
        )
        self.midiin.ignore_types(timing=False)
        self.midiout, self.port_out_name = open_midiport(
            -1,
            'output',
            client_name='euclid',
            port_name='euclid output_port'
        )
        self.midiin.set_callback(self.on_midi_in)

        self.octoeuclid = octoeuclid
        self.gate_len = gate_len

        self.ppqn = 24
        self._ppqn_count = 0

    def on_midi_in(self, event, data=None):

        message, dx = event

        if message == [248]:
            # MIDI clock
            if self._ppqn_count % self.ppqn == 0:
                print 'tick', self.step()
                self._ppqn_count = 0
            self._ppqn_count += 1
            return

        if message[:2] == [0x99, step_pads[0]] and message[2] > 0:
            # manual/sequenced step
            print 'step', self.step()
            return

        if message == [176, 51, 0]:
            # stop button
            self.reset()
            print 'reset all'
            return

        for idx in range(len(self.octoeuclid)):
            # controller mode only
            if message[:2] == [0xb0, rot_knobs[idx]]:
                self.octoeuclid.rotate(idx)
                print 'rotate', idx
                return
            if message[:2] == [0xb0, rst_knobs[idx]]:
                self.octoeuclid.reset(idx)
                print 'reset', idx
                return

            if message[1:2] == [gate_pads[idx]]:
                return

        if message in [[250], [251], [252]]: # transport
            return

        if message[:2] in [
            [176, 54],  # play button 127
            [176, 51],  # stop button 127
            [137, 44],  # step button 64!?
            [176, 123], # ??
            [177, 123], # ??
            [185, 123], # ??
        ]:
            return

        if message[0] in [144, 128]: # ??
            return

        print dx, message, data if data else ''

    def reset(self):
        for idx in range(len(self.octoeuclid)):
            self.octoeuclid.reset(idx)

    def step(self):
        fills = self.octoeuclid.step()
        notes = [gate_pads[i] for i in range(len(self.octoeuclid)) if fills[i]]
        for note in notes:
            self.midiout.send_message((0x99, note, GATE_HIGH))
        time.sleep(self.gate_len)
        for note in notes:
            self.midiout.send_message((0x89, note, GATE_LOW + 1))
        return notes

    def __str__(self):
        return 'BeatStepPro({0})'.format(len(self.octoeuclid))
