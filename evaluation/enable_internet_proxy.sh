#!/bin/bash
set -e

#####from DevCloud enable_internet_proxy.sh####

#/etc/profile用于login shell;/etc/bashrc用于non-login shell
config_files=("${HOME}/.bashrc")

for config_file in ${config_files[@]}
do
        sed -i '/^http_proxy=/d'  $config_file
        sed -i '/^https_proxy=/d'  $config_file
        sed -i '/^no_proxy=/d'  $config_file
        sed -i '/^export http_proxy/d'  $config_file

        echo >> $config_file
        echo "http_proxy=http://star-proxy.oa.com:3128" >> $config_file
        echo "https_proxy=http://star-proxy.oa.com:3128" >> $config_file
        echo "no_proxy=".woa.com,mirrors.cloud.tencent.com,tlinux-mirror.tencent-cloud.com,tlinux-mirrorlist.tencent-cloud.com,localhost,127.0.0.1,mirrors-tlinux.tencentyun.com,.oa.com,.local,.3gqq.com,.7700.org,.ad.com,.ada_sixjoy.com,.addev.com,.app.local,.apps.local,.aurora.com,.autotest123.com,.bocaiwawa.com,.boss.com,.cdc.com,.cdn.com,.cds.com,.cf.com,.cjgc.local,.cm.com,.code.com,.datamine.com,.dvas.com,.dyndns.tv,.ecc.com,.expochart.cn,.expovideo.cn,.fms.com,.great.com,.hadoop.sec,.heme.com,.home.com,.hotbar.com,.ibg.com,.ied.com,.ieg.local,.ierd.com,.imd.com,.imoss.com,.isd.com,.isoso.com,.itil.com,.kao5.com,.kf.com,.kitty.com,.lpptp.com,.m.com,.matrix.cloud,.matrix.net,.mickey.com,.mig.local,.mqq.com,.oiweb.com,.okbuy.isddev.com,.oss.com,.otaworld.com,.paipaioa.com,.qqbrowser.local,.qqinternal.com,.qqwork.com,.rtpre.com,.sc.oa.com,.sec.com,.server.com,.service.com,.sjkxinternal.com,.sllwrnm5.cn,.sng.local,.soc.com,.t.km,.tcna.com,.teg.local,.tencentvoip.com,.tenpayoa.com,.test.air.tenpay.com,.tr.com,.tr_autotest123.com,.vpn.com,.wb.local,.webdev.com,.webdev2.com,.wizard.com,.wqq.com,.wsd.com,.sng.com,.music.lan,.mnet2.com,.tencentb2.com,.tmeoa.com,.pcg.com,www.wip3.adobe.com,www-mm.wip3.adobe.com,mirrors.tencent.com,csighub.tencentyun.com,.cos-internal.ap-beijing.tencentcos.cn,.cos-internal.ap-shanghai.tencentcos.cn,.cos-internal.ap-guangzhou.tencentcos.cn,.cos-internal.ap-beijing-1.tencentcos.cn,.cos-internal.ap-qingyuan.tencentcos.cn,.cos-internal.ap-nanjing.tencentcos.cn,.cos-internal.ap-chengdu.tencentcos.cn,.cos-internal.ap-chongqing.tencentcos.cn,.cos-internal.ap-hongkong.tencentcos.cn,.cos-internal.ap-singapore.tencentcos.cn,.cos-internal.ap-mumbai.tencentcos.cn,.cos-internal.ap-jakarta.tencentcos.cn,.cos-internal.ap-seoul.tencentcos.cn,.cos-internal.ap-bangkok.tencentcos.cn,.cos-internal.ap-tokyo.tencentcos.cn,.cos-internal.na-siliconvalley.tencentcos.cn,.cos-internal.na-ashburn.tencentcos.cn,.cos-internal.na-toronto.tencentcos.cn,.cos-internal.sa-saopaulo.tencentcos.cn,.cos-internal.eu-frankfurt.tencentcos.cn,.cos-internal.eu-moscow.tencentcos.cn,.cos-internal.ap-taipei.tencentcos.cn,.cos-internal.ap-beijing.myqcloud.com,.cos-internal.ap-shanghai.myqcloud.com,.cos-internal.ap-guangzhou.myqcloud.com,.cos-internal.ap-beijing-1.myqcloud.com,.cos-internal.ap-qingyuan.myqcloud.com,.cos-internal.ap-nanjing.myqcloud.com,.cos-internal.ap-chengdu.myqcloud.com,.cos-internal.ap-chongqing.myqcloud.com,.cos-internal.ap-hongkong.myqcloud.com,.cos-internal.ap-singapore.myqcloud.com,.cos-internal.ap-mumbai.myqcloud.com,.cos-internal.ap-jakarta.myqcloud.com,.cos-internal.ap-seoul.myqcloud.com,.cos-internal.ap-bangkok.myqcloud.com,.cos-internal.ap-tokyo.myqcloud.com,.cos-internal.na-siliconvalley.myqcloud.com,.cos-internal.na-ashburn.myqcloud.com,.cos-internal.na-toronto.myqcloud.com,.cos-internal.sa-saopaulo.myqcloud.com,.cos-internal.eu-frankfurt.myqcloud.com,.cos-internal.eu-moscow.myqcloud.com,.cos-internal.ap-taipei.myqcloud.com"" >> $config_file

        echo "export http_proxy https_proxy no_proxy" >> $config_file

        source $config_file
done

echo "enable internet proxy success!"
