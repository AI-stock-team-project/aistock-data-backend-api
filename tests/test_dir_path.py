from pathlib import Path
from datetime import timedelta, datetime, timezone


def test():
    static_path = Path(__file__).resolve().parent.parent / 'static'
    dt = datetime.now().strftime('%Y%m%d_%H%M%S')
    trends_file_path = static_path / f'return_trends_{dt}.png'
    print(trends_file_path)
    # print(dt)


if __name__ == '__main__':
    test()
