from datetime import datetime, timedelta


class Time:
    def __init__(self):
        self.lunch_time = (datetime.min + timedelta(hours=12)).strftime("%I:%M %p")
        self.day_end = (datetime.min + timedelta(hours=17)).strftime("%I:%M %p")


class Track(Time):
    id = 0

    def __init__(self):
        super().__init__()
        Track.id += 1
        self.talks = {}
        self.sorted_talks_dict = Track.modify_input()

    # Extracting input in the form of title and minutes (return sorted input)
    @staticmethod
    def modify_input():

        talks = {}

        # Checking if file exists
        try:
            file = [i.strip() for i in open('test.txt')]

            # Split title and time duration from file
            for i in file:
                title, minutes = i.rsplit(maxsplit=1)
                try:
                    minutes = int(minutes[:-3])

                except ValueError:
                    minutes = 5
                talks[i] = minutes

        # Handling if file does not exist
        except FileNotFoundError as e:
            print("File not found ")

        # Sorting Talks in descending order

        sorted_talks = {key: value for key, value in sorted(talks.items(), key=lambda x: x[1], reverse=True)}
        return sorted_talks

    # Finding talks which can fill Sessions
    def find_talks(self, start_talk, end_talk):
        start = timedelta(hours=start_talk)
        for key, value in list(self.sorted_talks_dict.items()):
            # Calculating next talk timing
            next_time = start + timedelta(minutes=int(value))
            if next_time <= timedelta(hours=end_talk):
                self.talks[(datetime.min + start).strftime('%I:%M %p')] = key
                self.sorted_talks_dict.pop(key)
                start += timedelta(minutes=int(value))
        return self.talks

    # Display the Conference Track
    def display_output(self):
        while len(self.sorted_talks_dict) != 0:
            print('Track : %s \n' % Track.id)
            self.sessions(9, 12)
            print('%s - %s' % (self.lunch_time, 'Lunch'))
            self.sessions(13, 17)
            print('%s - %s \n' % (self.day_end, 'Networking Event'))
            Track.id += 1

    # Adjusting talks into different sessions and sorting
    def sessions(self, start, end):
        for time, title in sorted(self.find_talks(start, end).items()):
            print(time, '-', title)
        # clear previous entries
        self.talks.clear()


if __name__ == '__main__':
    a = Track()
    a.display_output()
