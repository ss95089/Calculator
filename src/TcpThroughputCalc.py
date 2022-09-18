import PySimpleGUI as sg
import math
import datetime

def main():
    col1 = [
        [sg.Text('RTT')],
        [sg.Text('PacketLoss')],
        [sg.Text('MTU')],
        [sg.Submit('Calculate')],
    ]
    col2 = [
        [sg.InputText(default_text='25', size =(10, 1), key='f01'), sg.Text('msec')],
        [sg.InputText(default_text='0.01', size=(10, 1), key='f02'), sg.Text("%")],
        [sg.InputText(default_text='1500', size=(10, 1), key='f03'), sg.Text("byte")],
    ]
    layout = [
        [
            [sg.Text('formula: (MSS/RTT)*(C/sqrt(PacketLoss))')],
            [sg.Column(col1, vertical_alignment='top'), sg.Column(col2, vertical_alignment='top'),],
            [sg.Output(size=(60, 10), font=('MS Gothic', 11), background_color='black', text_color='white')],
         ]
    ]
    window = sg.Window('TCP Throughput Calc', layout, finalize=True)

    while True:
        event, values = window.read()
        if event == 'Calculate':
            C = {'Pattern1 : C=sqrt(3/2)': math.sqrt(3/2), 'Pattern2 : C=1': 1, 'Pattern3 : C=1.2': 1.2, 'Pattern4 : C=1.22': 1.22}
            print(f"\n--- {datetime.datetime.now()} ---")
            for k, v in C.items():
                try:
                    rtt = float(values['f01']) / 1000
                    ploss = float(values['f02']) / 100
                    mtu = int(values['f03'])
                    r = ((mtu - 40) / rtt) * (v / math.sqrt(ploss))
                except:
                    sg.popup("Please enter the correct value.")
                    break
                else:
                    MbPerSec = round(r / 1000 ** 2, 2)
                    BytePerSec = MbPerSec * 8
                    print('■ {}'.format(k))
                    print("RTT {}ms , PacketLoss {}% , MTU {}byte".format(values['f01'], values['f02'], values['f03']))
                    print("maximum throughput : {}MB/sec ( {}Mbit/sec )".format(str(MbPerSec), str(BytePerSec)))
        if event == sg.WIN_CLOSED:
            break
    window.close()

if __name__ == '__main__':
    main()
