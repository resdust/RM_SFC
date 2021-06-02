## Preliminary
- clean you mininet env:
```
sudo mn -c
```
- change directory to src
```
cd src
python src/action2sqlite.py
```

## Start experiment
In RM_SFC directory:
1. start ryu manager
```
ryu-manager src/sfc_controller.py
```
2. init nfv network with mininet (Containernet)
```
sudo python src/containernet_sfc.py -n 10 --topo data/test.topo
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

ffmpeg -re -i ./dockers/Vedio.mp4 -c:a copy -c:v copy -f rtp_mpegts rtp://10.0.0.10:8888/live/vedio

```
# sfc_app修改内容

> Reference: [abulanov/sfc_app: Service Function Chaining Application for Ryu SDN controller](https://github.com/abulanov/sfc_app)

- Mininet只能使用当前系统shell作为虚拟主机，不方便安装其他功能

  修改Mininet为Containernet，并将host改为docker容器

- 部署的服务功能链无法自动显示报文信息，需要在节点的snort容器中手动开启数据包记录器。

  修改默认流表规则为转发到控制器，在控制器中加入打印报文信息的方法，打印信息后转交datapath。

- 部署的服务功能链没有实际功能，演示效果差。

  在其中两个节点安装ffplay和ffmpeg命令行工具，完成视频推流服务。

  （后改为在安装ffplay和ffmpeg命令后直接开启Mininet虚拟主机，因为找到的docker容器都只能直接运行命令，无法在xterm里手动打开，达不到演示效果）

- 添加和定义SFC流需要手动写入数据库，难以和迁移算法对接。

  编写把动作集拆分为服务流并写入数据库（service表）的自动化程序，每个状态下的动作集合表示为执行一条或多条服务流的部署。

问题：不能按照任意拓扑文件修改mininet虚拟网络拓扑，因为mininet控制器无法路由有环路的拓扑（1-2-3-1表示环路）。

解决：修改拓扑为简易拓扑，只能达到演示效果。***注意：手动修改了data/result10的route结果，仅为了实验演示，mapping结果未修改。***

