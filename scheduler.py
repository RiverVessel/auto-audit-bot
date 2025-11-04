import os
import subprocess


def run_audit_for_target(target):
    os.environ['TARGET_REPO'] = target
    subprocess.run(['python3', 'audit.py'], check=False)


def main():
    # Read targets from file
    if not os.path.exists('targets.txt'):
        print('No targets.txt found')
        return
    with open('targets.txt') as f:
        targets = [line.strip() for line in f if line.strip()]
    for target in targets:
        run_audit_for_target(target)


if __name__ == '__main__':
    main()
