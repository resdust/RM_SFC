## Preliminary
- clean you mininet env:
```
sudo mn -c
```
- change directory to src
```
cd src
```

## Start experiment
In RM_SFC directory:
1. start ryu manager
```
ryu-manager src/sfc_controller.py
```
2. init nfv network with mininet (Containernet)
```
sudo python src/containernet_sfc.py
```
3. update the flow rules through restful api
```shell
curl -i http://127.0.0.1:8080/add_flow/{n}
```
4. check the flow table
```
sudo ovs-ofctl -O OpenFlow13 dump-flows s{n}
```
5. play a vedio on the destination host and push the vedio from the source host

```shell
ffplay -i rtp://127.0.0.1:8888/live/vedio

ffmpeg -re -i ./Vedio.mp4 -c:a copy -c:v copy -f rtp_mpegts rtp://10.0.0.5:8888/live/vedio

```
