import re
import os

# TAG PATTERNS

open_sgl_tag = re.compile(r"(<( *[a-z]+ *)>)")
close_tag = re.compile(r"(</( *[a-z]+ *)>)")
open_multi_tag = re.compile(r"(< *([^<> ]+) +[^<>]+ *>)")
every_tag = re.compile(r"<[^<>]+>")  # not used


# ERROR MESSAGES

open_msg = "{}-tag is still open\n"
close_msg = "open {}-tag missing\n"

# CREATE FOLDER

cwd = os.getcwd()
if "XML Tag Logs" not in os.listdir(cwd):
    os.mkdir(os.path.join(cwd, "XML Tag Logs"))

dir_content = os.listdir(cwd)
xml_files = [file for file in dir_content if file.endswith(".xml")]

log_file_count = 0

for file in xml_files:

    tag_status = dict()
    ln = 0

    # for other xml files: consider changing encoding or delete attribute altogether to switch to "utf-8" (default)
    with open(file, "r", encoding="iso-8859-1") as xml_file:

        log_file = open("XML Tag Logs/{}_tags.txt".format(file[:-4]), "w")
        log_file_count += 1
        xml_file = xml_file.readlines()

        # FIRST LOOP REGISTERS ALL TAGS

        for line in xml_file:

            if re.findall(open_multi_tag, line):
                tag_kind = re.findall(open_multi_tag, line)[0][1]
                tag_status[tag_kind] = None

            if re.findall(open_sgl_tag, line):
                tag_kind = re.findall(open_sgl_tag, line)[0][1]
                tag_status[tag_kind] = None

            if re.findall(close_tag, line):
                tag_kind = re.findall(close_tag, line)[0][1]
                tag_status[tag_kind] = None

        # SECOND LOOP CHECKS IF OPEN OR CLOSED

        for line in xml_file:

            ln += 1

            if re.findall(open_sgl_tag, line):

                tag_kind = re.findall(open_sgl_tag, line)[0][1]
                if tag_status[tag_kind] == "open":
                    log_file.write("l. " + str(ln) + ": " +
                                   open_msg.format(tag_kind))
                else:
                    tag_status[tag_kind] = "open"

            if re.findall(open_multi_tag, line):

                tag_kind = re.findall(open_multi_tag, line)[0][1]
                if tag_status[tag_kind] == "open":
                    log_file.write("l. " + str(ln) + ": " +
                                   open_msg.format(tag_kind))
                else:
                    tag_status[tag_kind] = "open"

            if re.findall(close_tag, line):

                tag_kind = re.findall(close_tag, line)[0][1]
                if tag_status[tag_kind] == "closed" or tag_status[tag_kind] == None:
                    log_file.write("l. " + str(ln) + ": " +
                                   close_msg.format(tag_kind))
                tag_status[tag_kind] = "closed"

    # CHECK FOR OPEN TAGS BY END OF FILE

    log_file.write("\n")
    for tag_kind, status in tag_status.items():
        if status == "open":
            log_file.write(open_msg.format(tag_kind))

    # PRINT TAGS AND STATUS

    log_file.write("\n")
    for tag_kind, status in tag_status.items():
        log_file.write("{}: {}\n".format(tag_kind, status))

    log_file.close()

print("{} file(s) created in total".format(log_file_count))
print("Done")
