'''
python examples for working with subtitle files
'''
import webvtt
import pathlib
import datetime

def convert_srt_to_vtt(srt_path):
    '''
    converts SubRip (.srt) file to WebVTT (.vtt)
    '''
    input_path = pathlib.Path(srt_path)
    output_path = input_path.with_suffix('.vtt')
    vtt = webvtt.from_srt(input_path)
    vtt.save(output_path)

def convert_vtt_to_srt(vtt_path):
    '''
    converts WebVTT (.vtt) file to SubRip (.srt)
    '''
    input_path = pathlib.Path(vtt_path)
    output_path = input_path.with_suffix('.srt')
    vtt = webvtt.read(input_path)
    vtt.save_as_srt(output_path)

def shift_vtt(path, retime):
    '''
    shifts subtitle times
    i.e. retime=+5 = add five seconds to every start/ stop time
    ---- 00:01:00.000 becomes 00:01:05.000
    '''
    if (not "+" in retime and not "-" in retime) or \
        ("+" in retime and "-" in retime):
        print("friend, please supply either + or -")
        print("and an integer or float value")
        print("for the number of seconds to shift")
        print("to shift every sub 'back' five seconds, type:")
        print("-5")
    else:
        input_path = pathlib.Path(path)
        output_path = input_path.with_name(input_path.stem + '_retimed' + retime)
        vtt = webvtt.read(input_path)
        mod = float(retime.replace("+","").replace("-",""))
        for cue in vtt:
            start_time_orig = datetime.datetime.strptime(cue.start, "%H:%M:%S.%f")
            end_time_orig = datetime.datetime.strptime(cue.end, "%H:%M:%S.%f")
            if retime.startswith("+"):
                start_time_mod = datetime.timedelta(hours=start_time_orig.hour, minutes=start_time_orig.minute,\
                    seconds=start_time_orig.second, microseconds=start_time_orig.microsecond) + \
                    datetime.timedelta(seconds=mod)
                end_time_mod = datetime.timedelta(hours=end_time_orig.hour,minutes=end_time_orig.minute,\
                    seconds=end_time_orig.second,microseconds=start_time_orig.microsecond) + \
                    datetime.timedelta(seconds=mod)
            elif retime.startswith("-"):
                start_time_mod = datetime.timedelta(hours=start_time_orig.hour, minutes=start_time_orig.minute,\
                    seconds=start_time_orig.second, microseconds=start_time_orig.microsecond) - \
                    datetime.timedelta(seconds=mod)
                end_time_mod = datetime.timedelta(hours=end_time_orig.hour,minutes=end_time_orig.minute,\
                    seconds=end_time_orig.second,microseconds=start_time_orig.microsecond) - \
                    datetime.timedelta(seconds=mod)
            if len(str(start_time_mod)) == 14:
                start_time_mod = "0" + str(start_time_mod)[:-3]
            if len(str(end_time_mod)) == 14:
                end_time_mod = "0" + str(end_time_mod)[:-3]
            print(cue.start + " -> " + str(start_time_mod))
            print(cue.end + " -> " + str(end_time_mod))
            try:
                cue.start = str(start_time_mod)
                cue.end = str(end_time_mod)
            except webvtt.errors.MalformedCaptionError:
                cue.start = '00:00:00.000'
                cue.end = '00:00:00.001'
        vtt.save(output_path)
