# EXP-EMB002B-TRANSITION-V5-20260924

RQ-EMB-002 / H-EMB-002-B

Status: **SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL**
Mode: **prospective transition-resolution synthetic DATA**

Runs: 192
Paired seeds: 24
Ticks per run: 1000
Frozen delays: [0, 50, 60, 70, 80, 90, 100]

## Mean tracking RMSE

{
  "delay_0": 0.15951113438159922,
  "delay_100": 0.22990161866741132,
  "delay_50": 0.15248229021970777,
  "delay_60": 0.15644794244180224,
  "delay_70": 0.16513460155255996,
  "delay_80": 0.18554825378358722,
  "delay_90": 0.20834850524059756,
  "feedback_absent": 0.4764204741733329
}

## Primary rule checks

{
  "delay_100_degraded": true,
  "delay_50_within_tolerance": true,
  "delay_60_within_tolerance": true,
  "delay_90_degraded": true
}

Assay validity: True
Support rule satisfied: True

## Paired comparisons versus delay_0

{
  "delay_100": {
    "control": "delay_100",
    "differences_control_minus_delay_0": [
      0.0764905009637207,
      0.08018880764132788,
      0.07154614099059362,
      0.08628075649219566,
      0.06026656682510553,
      0.06728613301241981,
      0.07786332262713003,
      0.0621408159734636,
      0.06085477125809036,
      0.07386113018804633,
      0.05804296830539718,
      0.049535988666132624,
      0.0872939410819111,
      0.07748887438920637,
      0.0616812032132405,
      0.07724145268357197,
      0.08292069133164137,
      0.07579525228862752,
      0.062441317379555356,
      0.05893045187508103,
      0.07609838934416929,
      0.0767052925404639,
      0.05786910272389917,
      0.07054775106449954
    ],
    "fraction_delay_0_lower": 1.0,
    "maximum_difference": 0.0872939410819111,
    "mean_difference": 0.0703904842858121,
    "median_difference": 0.07270363558931997,
    "metric": "tracking_rmse_rad",
    "minimum_difference": 0.049535988666132624,
    "n_paired_seeds": 24,
    "p_value": null,
    "reference": "delay_0",
    "ties": 0
  },
  "delay_50": {
    "control": "delay_50",
    "differences_control_minus_delay_0": [
      -0.00487879412572062,
      -0.006361824791364795,
      -0.007727071025241644,
      -0.004816698308518663,
      -0.007636196624916464,
      -0.006111362095421985,
      -0.005963850157077288,
      -0.008054218078513503,
      -0.0050166138347589595,
      -0.00830862752618336,
      -0.0021298044356974355,
      -0.007144062647593236,
      -0.008514552629107053,
      -0.004955906723221437,
      -0.011306662369108988,
      -0.006380617641824737,
      -0.00923179131104429,
      -0.005713681417411215,
      -0.00974777476985772,
      -0.0068973512475931364,
      -0.008142989360359898,
      -0.00793867518191868,
      -0.008182857905872531,
      -0.007530275677067461
    ],
    "fraction_delay_0_lower": 0.0,
    "maximum_difference": -0.0021298044356974355,
    "mean_difference": -0.007028844161891462,
    "median_difference": -0.007337169162330348,
    "metric": "tracking_rmse_rad",
    "minimum_difference": -0.011306662369108988,
    "n_paired_seeds": 24,
    "p_value": null,
    "reference": "delay_0",
    "ties": 0
  },
  "delay_60": {
    "control": "delay_60",
    "differences_control_minus_delay_0": [
      -0.006369968697840261,
      0.0011155221106962931,
      0.005112529409131594,
      -0.002369796309012212,
      -0.0035728104224578283,
      -0.004362698057170961,
      -0.001564179387844672,
      -0.0006670085413607862,
      -0.003822410217903971,
      -0.004444245143643444,
      -0.003531309987682918,
      -0.008468675716505808,
      -0.0021160373285109835,
      -0.0022978834899231027,
      -0.005171335941212801,
      -0.007300301446287544,
      -0.004744379541411631,
      -0.005113720994226106,
      -0.0034034952657154005,
      -0.003214034464726262,
      -0.005154389491175804,
      -0.0010303635524462063,
      9.996523305588756e-05,
      -0.0011255793109531398
    ],
    "fraction_delay_0_lower": 0.125,
    "maximum_difference": 0.005112529409131594,
    "mean_difference": -0.0030631919397970026,
    "median_difference": -0.0034674026266991592,
    "metric": "tracking_rmse_rad",
    "minimum_difference": -0.008468675716505808,
    "n_paired_seeds": 24,
    "p_value": null,
    "reference": "delay_0",
    "ties": 0
  },
  "delay_70": {
    "control": "delay_70",
    "differences_control_minus_delay_0": [
      0.008460670231552558,
      0.007416762308180586,
      0.009057395452334804,
      0.008267999955532873,
      0.0001312779524656471,
      0.008297408082968,
      0.010865296219500498,
      0.007054942348329901,
      0.010127961050794193,
      0.0055387177645155605,
      0.009761278198655438,
      -0.0012343220336715477,
      0.006974156961822242,
      0.009237744644258306,
      -0.0007232314846440657,
      0.004858283240433692,
      0.007395749963292675,
      -0.000147577897688711,
      0.005338916636181246,
      -0.003517482876470329,
      0.010980356434690863,
      0.01413086779424233,
      -0.009082911916918068,
      0.005772953072698456
    ],
    "fraction_delay_0_lower": 0.7916666666666666,
    "maximum_difference": 0.01413086779424233,
    "mean_difference": 0.005623467170960714,
    "median_difference": 0.007225346155811288,
    "metric": "tracking_rmse_rad",
    "minimum_difference": -0.009082911916918068,
    "n_paired_seeds": 24,
    "p_value": null,
    "reference": "delay_0",
    "ties": 0
  },
  "delay_80": {
    "control": "delay_80",
    "differences_control_minus_delay_0": [
      0.027118551473287122,
      0.03023103256238699,
      0.028400224788088596,
      0.034632185361568646,
      0.019400253179053778,
      0.03619476428961252,
      0.022432421242100514,
      0.018326211430248818,
      0.02708468385142443,
      0.028353932468681287,
      0.026875581509378577,
      0.026388010569884573,
      0.03130356120387143,
      0.035399311522816085,
      0.018254322383253974,
      0.0192203519223616,
      0.0198785321980135,
      0.019998981012590927,
      0.012134884633311777,
      0.039096710202556284,
      0.03035696835698834,
      0.022890598829173436,
      0.02744099690983534,
      0.023477793747223807
    ],
    "fraction_delay_0_lower": 1.0,
    "maximum_difference": 0.039096710202556284,
    "mean_difference": 0.026037119401988013,
    "median_difference": 0.026980132680401503,
    "metric": "tracking_rmse_rad",
    "minimum_difference": 0.012134884633311777,
    "n_paired_seeds": 24,
    "p_value": null,
    "reference": "delay_0",
    "ties": 0
  },
  "delay_90": {
    "control": "delay_90",
    "differences_control_minus_delay_0": [
      0.04454360253132997,
      0.053530300601086406,
      0.05335426072242111,
      0.060366431994412995,
      0.04867410848318443,
      0.060292141442505526,
      0.05507720540185784,
      0.04608445153504881,
      0.06035658338968114,
      0.05344514445157775,
      0.05269127277718541,
      0.04111022054583183,
      0.04561806809238125,
      0.04452271293607135,
      0.05406552569097234,
      0.022410117192020157,
      0.05244076549171783,
      0.05757905726257395,
      0.028477992578389427,
      0.05517484553852642,
      0.06535270353557043,
      0.03356762907597449,
      0.030748616861551503,
      0.05261314248408708
    ],
    "fraction_delay_0_lower": 1.0,
    "maximum_difference": 0.06535270353557043,
    "mean_difference": 0.04883737085899831,
    "median_difference": 0.052652207630636244,
    "metric": "tracking_rmse_rad",
    "minimum_difference": 0.022410117192020157,
    "n_paired_seeds": 24,
    "p_value": null,
    "reference": "delay_0",
    "ties": 0
  },
  "feedback_absent": {
    "control": "feedback_absent",
    "differences_control_minus_delay_0": [
      0.3227823312452497,
      0.3121051182632165,
      0.3200814925402501,
      0.32385353373738646,
      0.30876649768592584,
      0.32169942942213536,
      0.32375304445236697,
      0.3115101556774611,
      0.31256028389458695,
      0.31108595326794297,
      0.31045946502697264,
      0.3079247290625994,
      0.3204981740727266,
      0.3243870626605714,
      0.3102036349607445,
      0.3221448212513674,
      0.32102601603683,
      0.3226513310713629,
      0.3102780868899224,
      0.3190873783652789,
      0.32228751784920534,
      0.3238860555170142,
      0.3117145889313143,
      0.31107745311917623
    ],
    "fraction_delay_0_lower": 1.0,
    "maximum_difference": 0.3243870626605714,
    "mean_difference": 0.3169093397917337,
    "median_difference": 0.3195844354527645,
    "metric": "tracking_rmse_rad",
    "minimum_difference": 0.3079247290625994,
    "n_paired_seeds": 24,
    "p_value": null,
    "reference": "delay_0",
    "ties": 0
  }
}

## Transition localization

{
  "degradation_margin_rad": 0.03,
  "earliest_registered_degraded_delay_ticks": 90,
  "fraction_required": 0.9,
  "localization_only_delays": [
    70,
    80
  ],
  "qualifying_delays_ticks": [
    90,
    100
  ]
}

## Integrity

{
  "all_seed_pairing_checks": true,
  "all_ticks_complete": true,
  "clean_source_freeze": true,
  "coverage": true,
  "run_count": true,
  "runtime_errors_absent": true
}

## Boundary

Prospective synthetic DATA for the new H-EMB-002-B timing-tolerance hypothesis derived from the earlier exploratory V4 curve. A supported result is limited to this fixed six-neuron joint fixture and the frozen effect-margin rules. It does not establish biological proprioception, general sensorimotor timing laws, real-device transfer, autonomy, consciousness, 5D superiority, independent replication, or scientific EVID. Human Review remains required.

No p-values were computed. The effect margins were frozen before V5 DATA.
Human Review remains PENDING. No automatic EVID promotion or independent
replication is claimed.
