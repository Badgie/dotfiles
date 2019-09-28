import subprocess

volume = subprocess.run(['pamixer', '--get-volume'], stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n', '')
mute = subprocess.run(['pamixer', '--get-mute'], stdout=subprocess.PIPE).stdout.decode('utf-8')

if 'false' in mute:
    print(f'VOL: {volume}%')
elif 'true' in mute:
    print(f'VOL: M')
