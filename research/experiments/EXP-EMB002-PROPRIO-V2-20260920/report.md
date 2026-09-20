# EXP-EMB002-PROPRIO-V2-20260920

RQ-EMB-002 / H-EMB-002-A

Status: **COMPLETED_EXPLORATORY_DATA**
Mode: **prospective exploratory proprioception DATA**

Source freeze: e479ee00bfc218e16596a63636ad0070d183483e
Runs: 80
Paired seeds: 20
Ticks per run: 1000
Delay: 20 ticks

## Mean outcomes

{
  "closed_loop": {
    "sensor_path_mean_abs_q_rad": 0.216407126020124,
    "sensor_path_rms_q_rad": 0.23282825813069605,
    "tracking_rmse_rad": 0.15885313367641699
  },
  "delayed_proprioception": {
    "sensor_path_mean_abs_q_rad": 0.22444120825416114,
    "sensor_path_rms_q_rad": 0.240768285130403,
    "tracking_rmse_rad": 0.15881078263797216
  },
  "feedback_absent": {
    "sensor_path_mean_abs_q_rad": 0.4578558377915436,
    "sensor_path_rms_q_rad": 0.524001041452353,
    "tracking_rmse_rad": 0.4763865809025666
  },
  "timing_shuffle": {
    "sensor_path_mean_abs_q_rad": 0.5269488275185457,
    "sensor_path_rms_q_rad": 0.5845305805938125,
    "tracking_rmse_rad": 0.47368862848399945
  }
}

## Paired descriptive comparisons

Positive control-minus-closed_loop differences mean lower error in intact
closed_loop proprioception. The primary H-EMB-002-A contrasts are
feedback_absent and delayed_proprioception. timing_shuffle is secondary.

[
  {
    "confirmatory_threshold_applied": false,
    "control": "feedback_absent",
    "differences_control_minus_closed_loop": [
      0.32294260365430666,
      0.3192637263068282,
      0.3216229247614103,
      0.32169631927146436,
      0.31087674918456876,
      0.32379418282036154,
      0.312089429347574,
      0.32007087867865514,
      0.317398388139279,
      0.32466068414743054,
      0.3190300653183724,
      0.31329540248614696,
      0.3111798427020912,
      0.3124346182105029,
      0.31263715565014905,
      0.3200361709351722,
      0.31224437264376265,
      0.312703205931378,
      0.32324326698867156,
      0.31944895734486656
    ],
    "fraction_closed_loop_lower": 1.0,
    "maximum_difference": 0.32466068414743054,
    "mean_difference": 0.3175334472261496,
    "median_difference": 0.3191468958126003,
    "metric": "tracking_rmse_rad",
    "minimum_difference": 0.31087674918456876,
    "n_paired_seeds": 20,
    "p_value": null,
    "predeclared_role": "primary",
    "reference": "closed_loop",
    "ties": 0
  },
  {
    "confirmatory_threshold_applied": false,
    "control": "feedback_absent",
    "differences_control_minus_closed_loop": [
      0.2923285392879662,
      0.29637221893902854,
      0.29032331861818883,
      0.2886017886005997,
      0.2870481656205713,
      0.29366462933437426,
      0.2865340560472391,
      0.2898815416045114,
      0.2949982363592409,
      0.2951030912582617,
      0.2932113273936164,
      0.28693809053618285,
      0.28863204566455736,
      0.28991420640895493,
      0.28845643058039794,
      0.29653003631818253,
      0.28617494751993044,
      0.2891019967332567,
      0.29650333770819615,
      0.29313766189988355
    ],
    "fraction_closed_loop_lower": 1.0,
    "maximum_difference": 0.29653003631818253,
    "mean_difference": 0.291172783321657,
    "median_difference": 0.2901187625135719,
    "metric": "sensor_path_rms_q_rad",
    "minimum_difference": 0.28617494751993044,
    "n_paired_seeds": 20,
    "p_value": null,
    "predeclared_role": "secondary",
    "reference": "closed_loop",
    "ties": 0
  },
  {
    "confirmatory_threshold_applied": false,
    "control": "delayed_proprioception",
    "differences_control_minus_closed_loop": [
      0.000839395769844764,
      -0.0007179848853265947,
      -0.0020572354476954824,
      -0.0020274701832228847,
      -0.0018268925697338123,
      0.0038284997180455527,
      -0.0016999166647929387,
      -0.003225003224285622,
      0.002186971760558487,
      0.0030011142311690553,
      0.0005770500295050329,
      0.0013637298531188613,
      -0.0032267225746037687,
      -0.0004309119139008222,
      -0.0015523138179865392,
      0.0015032747639169564,
      0.00017418585322359625,
      -0.0017057517299161051,
      0.0010782630001246463,
      0.0030706972630613616
    ],
    "fraction_closed_loop_lower": 0.5,
    "maximum_difference": 0.0038284997180455527,
    "mean_difference": -4.2351038444812805e-05,
    "median_difference": -0.00012836303033861296,
    "metric": "tracking_rmse_rad",
    "minimum_difference": -0.0032267225746037687,
    "n_paired_seeds": 20,
    "p_value": null,
    "predeclared_role": "primary",
    "reference": "closed_loop",
    "ties": 0
  },
  {
    "confirmatory_threshold_applied": false,
    "control": "delayed_proprioception",
    "differences_control_minus_closed_loop": [
      0.011863277861749233,
      0.014900051508019596,
      0.003030550328078141,
      0.0015502961245186797,
      0.004867936289489533,
      0.01394173871066734,
      0.0016594115649741503,
      0.0014812902905404213,
      0.011434594646134055,
      0.015663775095592747,
      0.009070720385774639,
      0.0043845978806725805,
      0.003150239119760062,
      0.005751774050715086,
      0.004672297832674005,
      0.011633624035470608,
      0.01110543709064718,
      0.004173020667229715,
      0.014594558550836356,
      0.009871347960594606
    ],
    "fraction_closed_loop_lower": 1.0,
    "maximum_difference": 0.015663775095592747,
    "mean_difference": 0.007940026999706936,
    "median_difference": 0.007411247218244862,
    "metric": "sensor_path_rms_q_rad",
    "minimum_difference": 0.0014812902905404213,
    "n_paired_seeds": 20,
    "p_value": null,
    "predeclared_role": "secondary",
    "reference": "closed_loop",
    "ties": 0
  },
  {
    "confirmatory_threshold_applied": false,
    "control": "timing_shuffle",
    "differences_control_minus_closed_loop": [
      0.3338658408801765,
      0.30966258294119153,
      0.3166951109030065,
      0.3271434791120664,
      0.30382387304742975,
      0.3309741309646158,
      0.3124140224514024,
      0.3219939287074721,
      0.3213912785227837,
      0.31927696768884806,
      0.31690008531627223,
      0.30103948396359537,
      0.30874128484117,
      0.3104941402564471,
      0.30802419248949287,
      0.31776836347464327,
      0.30281557332753284,
      0.3080800278830727,
      0.3155035638783653,
      0.31010196550206404
    ],
    "fraction_closed_loop_lower": 1.0,
    "maximum_difference": 0.3338658408801765,
    "mean_difference": 0.31483549480758244,
    "median_difference": 0.31395879316488384,
    "metric": "tracking_rmse_rad",
    "minimum_difference": 0.30103948396359537,
    "n_paired_seeds": 20,
    "p_value": null,
    "predeclared_role": "secondary",
    "reference": "closed_loop",
    "ties": 0
  },
  {
    "confirmatory_threshold_applied": false,
    "control": "timing_shuffle",
    "differences_control_minus_closed_loop": [
      0.35741339923739934,
      0.36416890466812624,
      0.3463309869455701,
      0.3534902780512168,
      0.34146012515039487,
      0.3597229929690649,
      0.35315512456449577,
      0.35796103861244477,
      0.3619794394158428,
      0.3465948412817042,
      0.34462047442640903,
      0.3449001884068574,
      0.35298585821152273,
      0.3550076265665423,
      0.3438962365438031,
      0.366587880083474,
      0.33663062024957713,
      0.34433606071502726,
      0.3568205776515092,
      0.34598379551134706
    ],
    "fraction_closed_loop_lower": 1.0,
    "maximum_difference": 0.366587880083474,
    "mean_difference": 0.35170232246311645,
    "median_difference": 0.3530704913880093,
    "metric": "sensor_path_rms_q_rad",
    "minimum_difference": 0.33663062024957713,
    "n_paired_seeds": 20,
    "p_value": null,
    "predeclared_role": "secondary",
    "reference": "closed_loop",
    "ties": 0
  }
]

## Integrity

{
  "all_seed_pairing_checks": true,
  "all_ticks_complete": true,
  "clean_source_freeze": true,
  "coverage": true,
  "identical_perturbation_contract": true,
  "run_count": true,
  "runtime_errors_absent": true
}

## Boundary

This is prospective exploratory synthetic DATA for the scoped H-EMB-002-A proprioception comparison. It is not confirmatory EVID, not independent replication, not evidence of learned body schema, autonomy, consciousness, biological equivalence, real-device transfer, or 5D superiority. Human Review remains required.

Human Review remains PENDING. No p-values or confirmatory support thresholds
were applied. No automatic EVID promotion or independent replication is claimed.
