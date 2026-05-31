# Ball Tracker Node

Pan-tilt kafa ile turuncu top takibi yapan ROS 2 node'u.

## Nasıl çalışır?

```
Kamera görüntüsü → HSV renk tespiti → Merkez hata → P kontrolör → JointTrajectory
```

## Parametre tablosu

| Parametre | Varsayılan | Açıklama |
|---|---|---|
| `kp_pan` | 0.8 | Yatay (sol-sağ) oransal kazanç |
| `kp_tilt` | 0.8 | Dikey (yukarı-aşağı) oransal kazanç |
| `pan_limit` | 1.57 rad | Pan açısı sınırı (±90°) |
| `tilt_limit` | 0.6 rad | Tilt açısı sınırı (±34°) |
| `min_ball_area` | 80 px² | Tespit için gereken minimum kontur alanı |

## İşaretleri terslemek

Kafa yanlış yöne dönerse `ball_tracker_node.py` satır 74-75'teki `+=`/`-=` işaretini değiştir.

## Çalıştırma (bağımsız)

```bash
ros2 run ball_tracker ball_tracker_node
# kazancı runtime'da değiştir:
ros2 param set /ball_tracker kp_pan 1.2
```

## Topic'ler

| Topic | Tip | Yön |
|---|---|---|
| `/camera/image_raw` | `sensor_msgs/Image` | Subscribe |
| `/head_controller/joint_trajectory` | `trajectory_msgs/JointTrajectory` | Publish |
