## shellmap

Shellmap is a tiny *pseudo-xargs* script that helps to chain or sequence variants of a shell command using placeholders.

### Usage

```
$ python shellmap.py "<base command with N placeholders>" "<placeholder 1>"
                                    "<placeholder 2>" ... "<placeholder N>" [--print|--run]
$ python shellmap.py --help
usage: shellmap.py [-h] [--print] [--run] N [N ...]

Chain/sequence shell scripts.

positional arguments:
  N           Command string with placeholders, followed by arguments.

optional arguments:
  -h, --help  show this help message and exit
  --print     Print the output commands
  --run       Run the output commands
```

### Format

Say we have the following directory structure:

```
month_reports/
    date_reports/
        15.csv
        16.csv
        17.csv
    Jan_2015.txt
    Feb_2015.txt
```

We wish to create a new directory *final_reports*, and make new files for each combination of the dates, months and one of *pre*, *curr*, and *post*, in the format DD_MMM_YYYY_[pre|curr|post].txt. The directory structure needs to be like this:

```
month_reports/
    final_reports/
        15_Jan_2015_pre.txt
        15_Jan_2015_curr.txt
        15_Jan_2015_post.txt
        16_Jan_2015_pre.txt
        16_Jan_2015_curr.txt
        16_Jan_2015_post.txt
        17_Jan_2015_pre.txt
        17_Jan_2015_curr.txt
        17_Jan_2015_post.txt
        15_Feb_2015_pre.txt
        15_Feb_2015_curr.txt
        15_Feb_2015_post.txt
        16_Feb_2015_pre.txt
        16_Feb_2015_curr.txt
        16_Feb_2015_post.txt
        17_Feb_2015_pre.txt
        17_Feb_2015_curr.txt
        17_Feb_2015_post.txt
    date_reports/
        15.csv
        16.csv
        17.csv
    Jan_2015.txt
    Feb_2015.txt
```

We have three positional arguments, one for the date, one for the month_year, and one for [pre|curr|post]. First we'd like to check the output commands to see what's going to run. So here's what we do:

```
$ mkdir final_reports && cd $_
$ shellmap "touch \$1@_\$2@_\$3@.txt" "15,16,17" "Jan_2015,Feb_2015" "pre,curr,post" --print
touch 15_Jan_2015_pre.txt
touch 15_Jan_2015_curr.txt
touch 15_Jan_2015_post.txt
touch 15_Feb_2015_pre.txt
touch 15_Feb_2015_curr.txt
touch 15_Feb_2015_post.txt
touch 16_Jan_2015_pre.txt
touch 16_Jan_2015_curr.txt
touch 16_Jan_2015_post.txt
touch 16_Feb_2015_pre.txt
touch 16_Feb_2015_curr.txt
touch 16_Feb_2015_post.txt
touch 17_Jan_2015_pre.txt
touch 17_Jan_2015_curr.txt
touch 17_Jan_2015_post.txt
touch 17_Feb_2015_pre.txt
touch 17_Feb_2015_curr.txt
touch 17_Feb_2015_post.txt
```

Great! The commands look valid. Time to run them.

```
$ shellmap "touch \$1@_\$2@_\$3@.txt" "15,16,17" "Jan_2015,Feb_2015" "pre,curr,post" --run
$ ls
15_Feb_2015_curr.txt  15_Jan_2015_curr.txt  16_Feb_2015_curr.txt  16_Jan_2015_curr.txt  17_Feb_2015_curr.txt  17_Jan_2015_curr.txt
15_Feb_2015_post.txt  15_Jan_2015_post.txt  16_Feb_2015_post.txt  16_Jan_2015_post.txt  17_Feb_2015_post.txt  17_Jan_2015_post.txt
15_Feb_2015_pre.txt   15_Jan_2015_pre.txt   16_Feb_2015_pre.txt   16_Jan_2015_pre.txt   17_Feb_2015_pre.txt   17_Jan_2015_pre.txt
```

Suh-weet! That worked. But wait, what if we have 31 date files in *date_reports* instead of 2? Do we have to type them all out in a comma-separated list? Why can't we just take the output of some shell command that will give us a list of those files? Like `ls`?

#### Shell commands within placeholders

Prefacing an argument list with `%` substitutes the list with the output of the command after the `%`. For instance, typing `"%ls date_reports/"` in our case would run `ls date_reports/`, take the output list, and place it there. Let's try that:

```
 $ python shellmap.py "touch \$1@_\$2@_\$3@.txt" "%ls ../date_reports/" "Jan_2015,Feb_2015" "pre,curr,post" --print
touch 15.csv_Jan_2015_pre.txt
touch 15.csv_Jan_2015_curr.txt
touch 15.csv_Jan_2015_post.txt
touch 15.csv_Feb_2015_pre.txt
touch 15.csv_Feb_2015_curr.txt
touch 15.csv_Feb_2015_post.txt
touch 16.csv_Jan_2015_pre.txt
touch 16.csv_Jan_2015_curr.txt
touch 16.csv_Jan_2015_post.txt
touch 16.csv_Feb_2015_pre.txt
touch 16.csv_Feb_2015_curr.txt
touch 16.csv_Feb_2015_post.txt
touch 17.csv_Jan_2015_pre.txt
touch 17.csv_Jan_2015_curr.txt
touch 17.csv_Jan_2015_post.txt
touch 17.csv_Feb_2015_pre.txt
touch 17.csv_Feb_2015_curr.txt
touch 17.csv_Feb_2015_post.txt
```

Seems to work, but there's that pesky *.csv* in that `ls` output. That's fine and dandy, we just have to use `sed` to get rid of that cruft. So here's the newer version:

```
$ python shellmap.py "touch \$1@_\$2@_\$3@.txt" "%ls -1 month_reports/date_reports/ | sed -e 's/\..*$//'" "Jan_2015,Feb_2015" "pre,curr,post" --print
touch 15_Jan_2015_pre.txt
touch 15_Jan_2015_curr.txt
touch 15_Jan_2015_post.txt
touch 15_Feb_2015_pre.txt
touch 15_Feb_2015_curr.txt
touch 15_Feb_2015_post.txt
touch 16_Jan_2015_pre.txt
touch 16_Jan_2015_curr.txt
touch 16_Jan_2015_post.txt
touch 16_Feb_2015_pre.txt
touch 16_Feb_2015_curr.txt
touch 16_Feb_2015_post.txt
touch 17_Jan_2015_pre.txt
touch 17_Jan_2015_curr.txt
touch 17_Jan_2015_post.txt
touch 17_Feb_2015_pre.txt
touch 17_Feb_2015_curr.txt
touch 17_Feb_2015_post.txt
```

And there we go!

### Downloading

```
$ git clone https://github.com/pranavrc/shellmap.git
$ cd shellmap/
$ python shellmap.py --help
usage: shellmap.py [-h] [--print] [--run] N [N ...]

Chain/sequence shell scripts.

positional arguments:
  N           Command string with placeholders, followed by arguments.

optional arguments:
  -h, --help  show this help message and exit
  --print     Print the output commands
  --run       Run the output commands
```

If you want the script to be globally executable, put it somewhere in your `$PATH`.

