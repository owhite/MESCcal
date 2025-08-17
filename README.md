## Problem with MESC json payload from log -fl command: 
### Expected
```
{
 'time': [0.0, 5e-05, 0.0001, 0.00015...],
 'Vbus.V.y1': [60.67, 60.59, 60.63, 60.67...],
 'Iu.I_phase.y1': [0.02, 0.02, 0.02, -0.21...],
 'Iv.I_phase.y1': [0.06, 0.06, 0.06, 0.06...],
 'Iw.I_phase.y1': [0.01, 0.01, -0.22, -0.22...],
 'Vd.V_dq.y1': [0.02, 0.0, 0.0, -0.01...],
 'Vq.V_dq.y1': [0.02, 0.0, 0.0, 0.02...],
 'angle.misc.y1': [57349, 57349, 57346, 57347...],
 "hall.misc.y1":[1,1,1,1...]}
}
```

### Actual
```
{
 'time': [0.0, 5e-05, 0.0001, 0.00015...],
 'Vbus.V.y1': [60.67, 60.59, 60.63, 60.67...],
 'Iu.I_phase.y1': [0.02, 0.02, 0.02, -0.21...],
 'Iv.I_phase.y1': [0.06, 0.06, 0.06, 0.06...],
 'Iw.I_phase.y1': [0.01, 0.01, -0.22, -0.22...],
 'Vd.V_dq.y1': [0.02, 0.0, 0.0, -0.01...],
 'Vq.V_dq.y1': [0.02, 0.0, 0.0, 0.02...],
 'angle.misc.y1': [57349, 57349, 57346, 57347...]
}
"hall.misc.y1":[1,1,1,1...]}
```
### Note that
- "hall.misc.y1" has double quotes, and single quote would be more consistent
- the array for hall.misc.y1 is outside of the payload
- the array for hall.misc.y1 is not in a closed bracket
