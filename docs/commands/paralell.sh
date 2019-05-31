# For VIPS
time seq 1 5 | xargs -n1 -P3 bash -c 'i=$0; cmd="large_conv"; url="http://localhost:8080/vips?run=${i}"; curl -d "cmd=$cmd&i=$i" -X POST $url'

time seq 1 5 | xargs -n1 -P3 bash -c 'i=$0; cmd="large_resize"; url="http://localhost:8080/vips?run=${i}"; curl -d "cmd=$cmd&i=$i" -X POST $url'

time seq 1 10 | xargs -n1 -P3 bash -c 'i=$0; cmd="medium_conv"; url="http://localhost:8080/vips?run=${i}"; curl -d "cmd=$cmd&i=$i" -X POST $url'

time seq 1 10 | xargs -n1 -P3 bash -c 'i=$0; cmd="medium_resize"; url="http://localhost:8080/vips?run=${i}"; curl -d "cmd=$cmd&i=$i" -X POST $url'

# For VIPS-CLI
time seq 1 5 | xargs -n1 -P3 bash -c 'i=$0; cmd="large_conv"; url="http://localhost:8080/vipscli?run=${i}"; curl -d "cmd=$cmd&i=$i" -X POST $url'

time seq 1 5 | xargs -n1 -P3 bash -c 'i=$0; cmd="large_resize"; url="http://localhost:8080/vipscli?run=${i}"; curl -d "cmd=$cmd&i=$i" -X POST $url'

time seq 1 10 | xargs -n1 -P3 bash -c 'i=$0; cmd="medium_conv"; url="http://localhost:8080/vipscli?run=${i}"; curl -d "cmd=$cmd&i=$i" -X POST $url'

time seq 1 10 | xargs -n1 -P3 bash -c 'i=$0; cmd="medium_resize"; url="http://localhost:8080/vipscli?run=${i}"; curl -d "cmd=$cmd&i=$i" -X POST $url'


# For Pillow
time seq 1 5 | xargs -n1 -P3 bash -c 'i=$0; cmd="large_conv"; url="http://localhost:8080/pillow?run=${i}"; curl -d "cmd=$cmd&i=$i" -X POST $url'

time seq 1 5 | xargs -n1 -P3 bash -c 'i=$0; cmd="large_resize"; url="http://localhost:8080/pillow?run=${i}"; curl -d "cmd=$cmd&i=$i" -X POST $url'

time seq 1 10 | xargs -n1 -P3 bash -c 'i=$0; cmd="medium_conv"; url="http://localhost:8080/pillow?run=${i}"; curl -d "cmd=$cmd&i=$i" -X POST $url'

time seq 1 10 | xargs -n1 -P3 bash -c 'i=$0; cmd="medium_resize"; url="http://localhost:8080/pillow?run=${i}"; curl -d "cmd=$cmd&i=$i" -X POST $url'
