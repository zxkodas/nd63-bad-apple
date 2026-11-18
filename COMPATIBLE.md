# Compatible keyboards

Only the **IROK ND63 MAX** (reports as "IROK ND_63", `3151:502d`, device id 3115) has been tested on
real hardware. The ND63 Ultra is said to be pretty much the same board, so it should work too. The
ND63 Pro has a different kind of RGB and is not supported.

In the vendor's own web app, the boards below use the ND63's protocol class (`CommonKBRY5088`), or
a subclass of it that doesn't change image upload or light-mode commands. Their chips vary (RY5088,
PAN1086, YC3121/YC3123). They upload custom images the same way (`0x0C`) and
offer the User Picture light mode (13). That makes the slideshow *likely* to work on them, but it
is **untested**, and the scripts are currently hardcoded to the ND63:

- the USB product id (`PID` in `nd63.py`), and
- the key map and physical layout (`MATRIX_KEYS` and `ROWS` in `gif.py`).

Porting to another board means changing those two things. Several boards share one USB id
(502d alone covers many of them), so the device id that `python3 nd63.py info` prints is what
identifies a board.

Source: the device list and protocol classes in the vendor web app, as extracted by
[monsgeek-akko-linux](https://github.com/echtzeit-solutions/monsgeek-akko-linux).

213 boards:

| Brand | Model | USB id | Device id | Firmware name |
|---|---|---|---|---|
| 凯酷 | KC68 | `3151:5029` | 2344 | `ry5088_kc68rt_dm` |
| 凯酷 | yumi17 | `3151:5025` | 2854 | `pan1086_yumi17_3m_1k` |
| 凯酷 | Yumi68 | `3151:5025` | 2855 | `pan1086_yumi68_soc` |
| 腹灵 | Air87 | `3151:5002` | 3022 | `yc3123_fl_k2503_soc` |
| 腹灵 | Blend HE | `3151:5029` | 2699 | `ry5088_k2402_dm_8k` |
| 腹灵 | GP75HE | `3151:502e` | 2869 | `yc3121_k242uk_3m_1k_1k` |
| 腹灵 | GP75HE | `3151:5030` | 2669 | `ry5088_k242_8k_8k` |
| 腹灵 | K239 UK | `3151:5029` | 2708 | `ry5088_k239_8k_dm_uk` |
| 腹灵 | K239 US | `3151:5029` | 2749 | `ry5088_k239_8k_dm` |
| 腹灵 | MK870 HE | `3151:5030` | 2703 | `ry5088_k258_8k_8k` |
| 腹灵 | NX68pro | `3151:5030` | 2447 | `ry5088_k2413a_soc_hall_8k_8k` |
| 腹灵 | NX87PRO | `3151:5002` | 2943 | `yc3123_fl_k245_3m_1k_soc` |
| 蚂蚁电竞 | AGK75 U2 | `3151:502f` | 2281 | `ry5088_agk75u2_soc_8k_002` |
| 蝴蝶 | B75 | `3151:502d` | 2928 | `ry5088_zdm_beat75v2_8k_dm` |
| 蝴蝶 | B98 | `3151:5030` | 3040 | `ry5088_zdm_k980_8k_1k` |
| Acrox | KM9 | `3151:5030` | 2893 | `ry5088_sy857_3m_8k_1k` |
| AIM1Keys | MATATAKI (US) | `3151:5029` | 2939 | `ry5088_mk825_dm_hall_8k` |
| AIM1Keys | MATATAKI(US Separate) | `3151:5029` | 3026 | `ry5088_nbd_mk25058_us_matataki_1m_8k` |
| AJAZZMOUSE | NS67 | `3151:502d` | 2810 | `ry5088_sg9038_8k_dm` |
| AJAZZMOUSE | NS67 PRO | `3151:502f` | 2746 | `ry5088_sg9038_8k_8k` |
| AJAZZMOUSE | NS87 | `3151:5030` | 3112 | `ry5088_sg9061_8k_soc` |
| akko | 5075 V3 | `3151:5002` | 3127 | `yc3123_akko_5075s_1m_1k` |
| akko | 5075 V3 HE | `3151:5030` | 3357 | `ry5088_akko_5075_v3_he_3m_8k_8k` |
| akko | 5075 V3 HE | `3151:502f` | 2807 | `ry5088_akko5075b_3m_8k_1k_1049es` |
| akko | 5075 VЗ HE | `3151:502d` | 3129 | `ry5088_akko_5075bv2he_1m` |
| akko | 5087 V3 | `3151:5002` | 3130 | `yc3123_akko_5087v2_1m_1k` |
| akko | 5087 V3 | `3151:5002` | 3095 | `yc3123_akko_5087v2_3m_1k` |
| akko | 5087 V3 HE | `3151:5029` | 3131 | `ry5088_akko_5087bv2he_1m_8k` |
| akko | 5087 V3 HE | `3151:5030` | 3359 | `ry5088_akko_5087_v3_he_3m_8k_8k` |
| akko | 5087 V3 HE | `3151:502f` | 2829 | `ry5088_akko_5087b_3m_8k_1k` |
| akko | 5087V3 HE TMR | `38ee:0001` | 3424 | `ry5088_akko_5087_v3_he_3m_8k_8k_v400` |
| akko | FUN60 KizunaAI SE | `3151:5029` | 3052 | `ry5088_akko_fun60_prob_jp_8k` |
| akko | FUN87 KizunaAI PE | `3151:5029` | 3187 | `ry5088_akko_5087hejp_1m_8k` |
| akko | K0039 | `3151:5030` | 2881 | `ry5088_k0039_8k_1k` |
| akko | MOD007 V5 HE | `3151:5030` | 3401 | `ry5088_akko_mod007_v5_he_b_3m_8k_8k_v500` |
| akko | MOD007 V5 HE | `3151:5029` | 3402 | `ry5088_akko_mod007_v5_he_b_1m_8k_8k_v500` |
| akko | MOD007 V5 HE | `3151:502f` | 2839 | `ry5088_akko_mod007_v5_3m_8k_8k` |
| akko | MOD007 V5 HE | `3151:5029` | 3113 | `ry5088_akko_mod007_v5_he_1m_8k` |
| akko | MOD007B V3-HE(UK) | `3151:5030` | 2872 | `ry5088_mod007sv3he_uk_8k_soc` |
| akko | MOD007B V3-HE(US) | `3151:5030` | 2871 | `ry5088_mod007sv3he_8k_soc` |
| akko | MOD007S V3-HE | `3151:5030` | 2683 | `ry5088_mod007sv3he_dm_8k` |
| akko | MOD007S V3-HE UK | `3151:5029` | 3322 | `ry5088_akko_mod007sv3he_uk_b_1m_8k` |
| akko | MOD007S V3-HE UK | `3151:5030` | 2704 | `ry5088_mod007sv3he_uk_8k_dm` |
| akko | MOD007S V3-HE US | `3151:5029` | 3321 | `ry5088_akko_mod007sv3he_us_b_1m_8k` |
| akko | MOD68 | `3151:5030` | 3162 | `ry5088_akko_mod68_8k_8k_3m` |
| akko | MOD68 | `3151:5029` | 3163 | `ry5088_akko_mod68_8k_1m` |
| akko | MOD68 | `3151:5029` | 3397 | `ry5088_akko_mod68_3m_8k_8k_v400` |
| akko | MOD68 UK | `3151:5030` | 3341 | `ry5088_akko_mod68_uk_8k_8k_3m` |
| akko | MOD68 UK | `38ee:0009` | 3378 | `ry5088_akko_mod68_uk_8k_1m_v500` |
| akko | TAC75 HE | `3151:502d` | 2782 | `ry5088_akko_tac75he_8k_dm` |
| akko | TAC87 | `3151:5030` | 3200 | `ry5088_akko_tac87_1m_8k` |
| akko | TAC87 | `3151:5002` | 2786 | `yc3123_5087sv3_8k_1k` |
| AttackShark | K85 | `3151:502d` | 2552 | `ry5088_sg_sg8948g_1m_8k` |
| AttackShark | R75PROHE | `3151:502f` | 2756 | `ry5088_sg8995_3m_8k_1k` |
| AttackShark | R82HE | `3151:502d` | 2844 | `ry5088_zdm_r82_dm` |
| AttackShark | R82PROHE | `3151:502f` | 2798 | `ry5088_zdm_r82_8k_1k` |
| AttackShark | R86PROHE | `3151:5030` | 2793 | `ry5088_sg8967_8k_1k` |
| AttackShark | X60 | `3151:5029` | 2929 | `ry5088_nbd_mk666v2_1m_8k` |
| AttackShark | X65 | `3151:5029` | 2942 | `ry5088_sg_sg9023_1m_8k` |
| AttackShark | X65HE | `3151:502d` | 2268 | `ry5088_sg9023_dm_8k_rt002` |
| AttackShark | X65PRO | `3151:502f` | 2308 | `ry5088_sg9006_8k_002` |
| AttackShark | X65PRO | `3151:5030` | 2938 | `ry5088_sg_sg9006_3m_8k_1k` |
| AttackShark | X68HE | `3151:502d` | 2270 | `ry5088_x68rt004_8k_dm` |
| AttackShark | X68HE | `3151:502d` | 2902 | `ry5088_x68v2_8k_dm` |
| AttackShark | X68HE | `3151:502d` | 2472 | `ry5088_x682_8k_dm` |
| AttackShark | X68PRO HE | `3151:502f` | 2901 | `ry5088_x68v2_8k` |
| AttackShark | X68PRO HE | `3151:502f` | 2370 | `ry5088_x68_8k_002` |
| AttackShark | X820Ultra | `3151:5002` | 2804 | `yc3123_sg9045_soc` |
| AttackShark | X82PRO HE | `3151:502f` | 2356 | `ry5088_sg_sg9015_3m_8k` |
| AttackShark | X85MAX | `3151:5002` | 2864 | `yc3123_zyl_x85max_3m_1k` |
| AttackShark | X85Ultra | `3151:5030` | 2769 | `ry5088_zdm_zyl_x85ultra_8k_1k_3m` |
| AttackShark | X87Ultra | `3151:502d` | 2660 | `ry5088_sg9035_8k_1k_soc` |
| AttackShark | X87Ultra | `3151:5030` | 2852 | `ry5088_sg9035_3m_8k_1k` |
| cherry | MX8.2 | `046a:012d` | 2494 | `ry5088_cherrymx82_8k_8k` |
| DNS | GP87HE | `3151:5029` | 2957 | `ry5088_k228_8k_dm` |
| EDRA | EK368RT | `3151:5030` | 2835 | `ry5088_sg9004_8k_1k` |
| EPOMAKER | Epomaker 65 | `3151:502d` | 2870 | `ry5088_epomaker65_dm_8k` |
| EPOMAKER | G84 HE | `3151:5030` | 2642 | `ry5088_fq_x122_rt001_3m_8k_8k` |
| EPOMAKER | HE68 Llte | `3151:5029` | 2883 | `ry5088_hf_kf109_1m_8k` |
| EPOMAKER | HE68 Llte | `3151:5029` | 2762 | `ry5088_hf_kf109_1m_8k` |
| EPOMAKER | HE68 Llte | `3151:5030` | 2761 | `ry5088_hf_kf109_3m_8k_1k` |
| EPOMAKER | HE75 Mag | `3151:502f` | 2520 | `ry5088_x87a_he75mag_8k_8k_002` |
| EPOMAKER | KIIBOOM-68C | `3151:502d` | 2586 | `ry5088_kiiboom68c_dm_8k` |
| EPOMAKER | RT75 | `3151:5002` | 3059 | `yc3123_hf_kf107_3m_oled_1k_rgb_kb_soc_v100` |
| EPOMAKER | RT85 | `3151:5002` | 2895 | `yc3123_ss_sn001` |
| EWEADNV | DEEP68 | `3151:5025` | 2578 | `ry5088_x111_8k_1k` |
| EWEADNV | DEEP68 | `3151:5030` | 2710 | `ry5088_x111a_3m_8k_8k` |
| EWEADNV | DEEP68 | `3151:5029` | 2711 | `ry5088_x111c_1m_8k` |
| EWEADNV | DEEP80 | `3151:5030` | 2652 | `ry5088_fq_x110a_3m_8k_8k` |
| EWEADNV | DEEP80 | `3151:5030` | 2574 | `ry5088_x110b_deep80_8k_1k` |
| EWEADNV | DEEP80 | `3151:5029` | 2653 | `ry5088_fq_x110c_1m_8k` |
| EWEADNV | K68 | `3151:502d` | 2301 | `ry5088_k80_dm_8k_002` |
| EWEADNV | SMART 875 | `3151:5030` | 2637 | `ry5088_smart875he_8k_8k` |
| EWEADNV | V82 RGB | `3151:5025` | 2296 | `pan1086_k60s_soc` |
| EWEADNV | V99 | `3151:5025` | 2279 | `pan1086_k62_soc` |
| EWEADNV | V99 | `3151:5025` | 2297 | `pan1086_k63_soc` |
| EWEADNV | ZAP68 | `3151:5030` | 3036 | `ry5088_zdm_zap68_v2_3m_8k_1k` |
| EWEADNV | ZAP68 | `3151:5030` | 2426 | `ry5088_zap68_8k_1k_hall` |
| EWEADNV | ZAP68 | `3151:502d` | 2348 | `ry5088_battle68pro_dm_8k_hall_002` |
| EWEADNV | ZAP68Ultra | `3151:5030` | 2510 | `ry5088_zap68ultra_8k_8k_hall` |
| EWEADNV | ZAP87 | `3151:5030` | 2527 | `ry5088_zap87_8k_1k_002` |
| FREEWOLF | F68 | `3151:5030` | 2634 | `ry5088_zdm_zyl_free_wolf_f68_1m_1k` |
| FREEWOLF | F68 PRO | `3151:5030` | 2594 | `ry5088_zdm_zyl_free_wolf_f68_3m_8k_1k` |
| gamakay2 | LK75 | `3151:5030` | 2808 | `ry5088_hf_kf810_ry1049es_8k_1k` |
| gamakay2 | LK75 | `3151:5030` | 2709 | `ry5088_hf_kf810_3m_8k_1k` |
| gamakay2 | NS68 | `3151:502d` | 2572 | `ry5088_yx_k80_ns68_1m_8k_rt002` |
| gamakay2 | NS68 | `3151:502f` | 2638 | `ry5088_k80ns68_8k_1k_002` |
| GAMEPOWER | TIRUS HE80 | `3151:5030` | 3108 | `ry5088_mk231v2_uk_8k_dm` |
| Gamepro | MK160B MAX | `3151:502d` | 2930 | `ry5088_sg_sg8948_1m_8k` |
| GKX68MAGNUM | Gaming Keyboard | `3151:5033` | 2820 | `ry5088_mk806b_8k_machine` |
| GTUNE | GMK-82 | `3151:5029` | 2912 | `ry5088_zw_gmk82jp_1m_8k` |
| GVSTONE | GV10M-8K | `3151:5033` | 2727 | `ry5088_hc_gv10m_3m_8k` |
| GVSTONE | GV8M-8K | `3151:5033` | 2801 | `ry5088_gv8m_8k_machine` |
| Hator | GEO65HE | `379a:1803` | 2791 | `ry5088_k2404_uk_3m_8k_8k` |
| Hator | HTK1160 | `3151:5002` | 3049 | `yc3123_k2506mxb_us_dm` |
| Hator | HTK1160UA | `379a:1805` | 2909 | `yc3123_k2506mxa_1m_1k_soc` |
| Hator | HTK1180UA | `379a:1805` | 2774 | `yc3123_k2505_1m_1k_soc` |
| Hator | HTK1860 | `379a:1803` | 2918 | `ry5088_k2506he_b_us_8k_dm` |
| Hator | HTK1860UA | `379a:1803` | 2917 | `ry5088_k2506he_a_ua_8k_dm` |
| Hator | HTK1880 | `379a:1803` | 2856 | `ry5088_k2505he_ua_1m_8k` |
| Hator | HTK1880UA | `379a:1803` | 2853 | `ry5088_k2505he_ua_1m_8k` |
| Hator | HTK3160 | `379a:1805` | 3051 | `yc3123_k2506mxd_us_soc` |
| Hator | HTK3160UA | `379a:1805` | 2823 | `yc3123_k2506mxc_ua_soc` |
| Hator | HTK3180 | `379a:1805` | 3045 | `yc3123_k2505_3m_1k_soc` |
| Hator | HTK3180UA | `379a:1805` | 2759 | `yc3123_k2505_3m_1k_soc` |
| Hator | HTK3860 | `379a:1803` | 2919 | `ry5088_k2506he_c_3m_8k_8k` |
| Hator | HTK3860EU | `379a:1803` | 2920 | `ry5088_k2506hee_uk_3m_8k_8k` |
| Hator | HTK3860UA | `379a:1803` | 2876 | `ry5088_k2506he_c_3m_8k_8k` |
| Hator | HTK3880 | `379a:1803` | 2857 | `ry5088_k2505_8k_8k` |
| Hator | HTK3880EU | `379a:1803` | 2858 | `ry5088_k2505hee_8k_uk` |
| Hator | HTK3880UA | `379a:1803` | 2800 | `ry5088_k2505_8k_8k` |
| Hator | HTK4160 | `3151:5002` | 3047 | `yc3123_k2506mxe_3m_1k_soc` |
| Hator | HTK4160UA | `379a:1806` | 2910 | `yc3123_k2506mxe_3m_1k_soc` |
| Hator | HTK4180 | `379a:1805` | 3046 | `yc3123_k2505_soc` |
| Hator | HTK4180EU | `379a:1805` | 2862 | `yc3123_k2505uk_3m_1k_soc` |
| Hator | HTK4180UA | `379a:1806` | 2861 | `yc3123_k2505_soc` |
| Hator | K2405 | `379a:1803` | 2806 | `ry5088_k2405_uk_3m_8k_8k` |
| Keydous | NJ98-CP | `3151:502f` | 2576 | `ry5088_nj98cp_8k_8k_002` |
| LOMZHUBWEB | Lomz 75S | `3151:502d` | 2828 | `ry5088_mk25032_8k_dm` |
| MageGee | Gaming Keyboard | `3151:5029` | 2848 | `ry5088_nbd_mk826_1m_8k` |
| MageGee | Gaming Keyboard | `3151:5030` | 2887 | `ry5088_nbd_mk25023a_3m_8k_1k` |
| MageGee | Gaming Keyboard | `3151:5030` | 2775 | `ry5088_nbd_mk25023_3m_8k_1k` |
| MageGee | Gaming Keyboard | `3151:5030` | 2677 | `ry5088_nbd_mk902_3m_8k_1k` |
| MageGee | MK-BOX | `3151:502c` | 2311 | `yc3121_mk606_68k_dm_hall_v300` |
| MageGee | MK25020 | `3151:5030` | 2740 | `ry5088_nbd_mk25020_3m_8k_1k` |
| MageGee | MK25022 | `3151:5030` | 2712 | `ry5088_nbd_mk25022b_3m_8k_1k` |
| Mambasnake | M82HE | `3151:502d` | 2335 | `ry5088_sg_sg9015_1m_8k` |
| Mambasnake | X60HE | `3151:502f` | 2368 | `ry5088_mk666_soc_8k_002` |
| MICROPACK | K-68M | `3151:502d` | 2546 | `ry5088_k80a_dm_8k_002` |
| MonsGeek | FUN60 PRO | `3151:5030` | 2785 | `ry5088_akko_fun60_3m_8k_1k` |
| MonsGeek | FUN75 | `3151:502d` | 2648 | `ry5088_mgk_fun75_8k_dm` |
| NOPPOO | X68 | `3151:5002` | 2896 | `yc3123_cx_3m_1k` |
| NyfterUG | Nyf HE 82K | `3151:502f` | 2752 | `ry5088_osd_dk82_uk_3m_8k_8k` |
| PIIFOXDRIVER | DEFENDER 68 | `3151:502d` | 2499 | `ry5088_kf109_defender68_1m_8k` |
| PLUXKB | PLUX CST KB | `3151:5030` | 2817 | `yc3123_osd_k986_3m_1k_soc` |
| rongyuan | Beat75 | `3151:5030` | 2976 | `ry5088_zdm_beat75v2_lovely_8k` |
| rongyuan | DK82 HE | `3151:502f` | 2690 | `ry5088_osd_dk82_3m_8k_8k` |
| rongyuan | FF101 | `3151:5033` | 2342 | `ry5088_hc_ff101_machine` |
| rongyuan | Gaming Keyboard | `3151:5029` | 2899 | `ry5088_nbd_mk25051b_1m_8k` |
| rongyuan | Gaming Keyboard | `3151:502f` | 2892 | `ry5088_x87a_dy_8k_8k_002` |
| rongyuan | GK75 | `3151:5029` | 3075 | `ry5088_kf304b_1m_8k` |
| rongyuan | IROK ND_63 (ND63 MAX **tested**, Ultra likely) | `3151:502d` | 3115 | `ry5088_jc_gk8145g_1m_8k` |
| rongyuan | K67 | `3151:5029` | 2723 | `ry5088_mopao_k67_1m_8k` |
| rongyuan | K860 | `3151:5002` | 2958 | `yc3123_gjy_k860_3m_1k_soc` |
| rongyuan | KF068 | `3151:5029` | 2278 | `ry5088_xs_kf068_dm_8k` |
| rongyuan | KF068 | `3151:5029` | 2338 | `ry5088_xs_2338` |
| rongyuan | Lomz 75S | `3151:5029` | 2737 | `ry5088_mk25031_dm_8k` |
| rongyuan | MK-23 | `3151:5030` | 2766 | `ry5088_sg9000_3m_8k_1k` |
| rongyuan | MK129 | `3151:5029` | 2763 | `ry5088_gzs_mk129us_1m_8k` |
| rongyuan | Phantom X68PG | `3151:502c` | 3038 | `yc3121_youxiang_k80c_1m_1k_ry1049e` |
| rongyuan | Phantom X68RB | `3151:502c` | 3037 | `yc3121_youxiang_k80c_1m_1k_ry1049e` |
| rongyuan | SG8905 | `3151:5030` | 2776 | `ry5088_sg8905_3m_8k_1k` |
| rongyuan | SG8992 | `3151:5030` | 2772 | `ry5088_sg8992_3m_8k_1k` |
| rongyuan | X107 | `3151:502d` | 2386 | `ry5088_fq_x107_1m_8k` |
| ROYALAXE | XL98 | `3151:5002` | 2925 | `yc3123_lj_xl98_soc` |
| SPYSELF | H60 | `3151:5029` | 2866 | `ry5088_yh_h60_1m_8k` |
| SUNROSE | JK82-1 | `3151:5030` | 2916 | `ry5088_bd_jk82_3m_8k_1k` |
| sunsonny | N-J100 | `3151:502d` | 2780 | `ry5088_sg8948j_dm_8k_002` |
| SUPER68 | SUPER68 | `3151:5029` | 2879 | `ry5088_hf_kf068_1m_8k` |
| SUPER68 | SUPER75 | `3151:5029` | 2802 | `ry5088_kf304_dm_8k` |
| TITANHUB | TITAN60 | `3151:5029` | 2220 | `ry5088_mk658_dm_8k_hall` |
| TITANHUB | TITAN68HE | `3151:5029` | 2116 | `ry5088_mk636_dm_8k_hall` |
| VGNNEON | Neon75 | `3151:502d` | 2904 | `ry5088_jc_gk8640g_1m_8k` |
| VGNNEON | Neon75 | `3151:502f` | 2781 | `ry5088_jc_gk6980gw_8k_8k` |
| VGNNEON | Neon75 | `3151:502f` | 2905 | `ry5088_jc_gk8640w_ulter_3m_8k_8k` |
| VGNNEON | Neon75 | `3151:502f` | 2859 | `ry5088_jc_gk8640w_8k_8k` |
| VKMS | MAG75 Max | `3151:5030` | 2398 | `ry5088_fq_x78_3m_8k_8k` |
| VKMS | Mecha 75 | `374a:a242` | 2700 | `yc3123_nbd_mk25037_1M_1K` |
| VKMS | NB68 | `374a:a228` | 2560 | `ry5088_fq_ns68_3m_8k_8k_rt002` |
| VKMS | NB68 Max | `374a:a236` | 2757 | `ry5088_fq_x82vk_nb68max_3m_8k_8k` |
| VKMS | NB68 Max | `374a:a236` | 3111 | `ry5088_0001_fq_x82_vk_nb68_max_3m_8k_8k` |
| VKMS | VK 75 PRO | `374a:a250` | 2963 | `yc3123_fq_x87_mag75_3m_1k_soc` |
| VKMS | VK MAG 75 | `374a:a216` | 2246 | `ry5088_x78rt001_mag75_8k_dm` |
| VKMS | VK MAG68 | `374a:a225` | 2320 | `ry5088_x118mag68_dm_8k_002` |
| VKMS | VK MAG75 Lite | `374a:a213` | 2234 | `ry5088_x78rt004_mag75_8k_dm` |
| VKMS | VK MAG75 Pro | `374a:a216` | 2227 | `ry5088_x78rt001_mag75_8k_dm` |
| VKMS | VK99 | `3151:5030` | 2410 | `ry5088_fq_vk99_3m_8k` |
| VKMS | VK99 Gaming | `374a:a219` | 2831 | `ry5088_fq_vk99_8k_8k` |
| WINSTAR | RK-X44-67 | `3151:502d` | 2796 | `ry5088_sg9023b_dm_8k_002` |
| XinMengK65Keyboard | Beat65-keyboard | `3151:502d` | 2326 | `ry5088_k65rt002_dm_hall_8k` |
| XinMengK65Keyboard | Beat65-keyboard | `3151:502f` | 2436 | `ry5088_beat65_8k_1k_002` |
| XinMengK65Keyboard | Beat65-keyboard | `3151:502d` | 2535 | `ry5088_beat652_8k_dm_002` |
| XinMengK65Keyboard | Beat68-keyboard | `3151:502f` | 2590 | `ry5088_zdm_xm_beat68_3m_8k_1k` |
| XinMengK65Keyboard | Beat68-keyboard | `3151:5030` | 2671 | `ry5088_zdm_xm_beat68elite_8k_1k` |
| XinMengK65Keyboard | Beat68-keyboard | `3151:502d` | 2589 | `ry5088_zdm_xm_beat68_1m_8k` |
| XinMengK65Keyboard | Beat68-keyboard | `3151:502f` | 2680 | `ry5088_zdm_xm_beat68_3m_8k_8k` |
| XinMengK65Keyboard | Beat75 | `3151:5030` | 2770 | `ry5088_zdm_beat75v2_8k_8k_3m` |
| XinMengK65Keyboard | Beat75 | `3151:502d` | 2797 | `ry5088_zdm_beat75v2_8k_dm` |
| XinMengK65Keyboard | K980 | `3151:5030` | 2795 | `ry5088_zdm_k980_8k_1k` |
| XinMengK65Keyboard | K982D | `3151:5030` | 2731 | `ry5088_zmd_k982d_3m_1k` |
| YUNZII | AL75 PRO | `3151:5002` | 2923 | `yc3123_nbd_mk830_al75_3m_1k_soc` |
| YUNZII | Gaming Keyboard | `3151:5029` | 2834 | `ry5088_nbd_mk825_1m_8k` |
| YUNZII | RT75PRO | `3151:5030` | 2865 | `ry5088_zmd_k982d_3m_8k_1k` |
