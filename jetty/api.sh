grep -E "\/discuss\/saveDiscuss|\/discussComment\/saveDiscussComment" /data/webapp/api/logs/2016_10_05.request.log| awk  '{print $1}' | sort -nr | uniq -c| sort -nr
