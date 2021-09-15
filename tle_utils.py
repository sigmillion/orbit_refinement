from random import uniform, random, randrange

# Parse TLE
def line1_to_param(line):
    line_num = line[0]
    sat_num = line[2:8]
    launch_info = line[9:17]
    epoch_yr = line[18:20]
    epoch_day = float(line[20:32])
    mmd = line[33:43]
    mmdd = line[44:52]
    drag = line[53:61]
    eff_type = line[62]
    eset_num = line[64:68]
    check_sum = line[68]
    return line_num, sat_num, launch_info, epoch_yr, epoch_day, mmd, mmdd, drag, eff_type, eset_num, check_sum

def line2_to_param(line):
    line_num = line[0]
    sat_num = line[2:7]  # satellite catalog number
    inclination = float(line[8:16])  # [degrees]
    raan = float(line[17:25])  # right ascension of ascending node [degrees]
    eccentricity = float('0.' + line[26:33])  # (decimal point assumed)
    ap = float(line[34:42])  # argument of perigee [degrees]
    ma = float(line[43:51])  # mean anomaly [degrees]
    mm = float(line[52:63])  # mean motion [revolutions/day]
    rev_num = line[63:68]  # revolution number at epoch
    check_sum = int(line[68])  # check sum (add digits mod 10, '-' = 1)
    return line_num, sat_num, inclination, raan, eccentricity, ap, ma, mm, rev_num, check_sum

def tle2vec(line1,line2):
    (line_num, sat_num, launch_info, epoch_yr, epoch_day, mmd, mmdd, drag, eff_type, eset_num, check_sum) = line1_to_param(line1)
    (line_num, sat_num, inclination, raan, eccentricity, ap, ma, mm, rev_num, check_sum) = line2_to_param(line2)
    return inclination, raan, ap, mm
    # return inclination, raan, ap, ma, mm
    # return inclination, raan, ap, ma, epoch_day

def tle2elements(line1,line2):
    (line_num, sat_num, launch_info, epoch_yr, epoch_day, mmd, mmdd, drag, eff_type, eset_num, check_sum) = line1_to_param(line1)
    (line_num, sat_num, inclination, raan, eccentricity, ap, ma, mm, rev_num, check_sum) = line2_to_param(line2)
    return inclination, raan, eccentricity, ap, ma, mm
    # return inclination, raan, ap, ma, epoch_day

def build_line1(line_num, sat_num, launch_info, epoch_yr, epoch_day, mmd, mmdd, drag, eff_type, eset_num):
    # Convert numbers to strings
    epoch_day = f'{epoch_day:12.8f}'

    # Reconstruct TLE string
    out = line_num + ' ' + sat_num + ' ' + launch_info + ' ' + \
          epoch_yr + epoch_day + ' ' + mmd + ' ' + mmdd + ' ' + \
          drag + ' ' + eff_type + ' ' + eset_num

    # Add checksum
    out = add_check_sum(out)
    return out

def build_line2(line_num, sat_num, inclination_new, raan_new, eccentricity_new, ap_new, ma_new, mm_new, rev_num):
    # Convert numbers to strings
    inclination = f'{inclination_new:8.4f}'
    raan = f'{raan_new:8.4f}'
    eccentricity_new = f'{eccentricity_new:9.7f}'
    eccentricity = eccentricity_new[2:9]
    ap = f'{ap_new:8.4f}'
    ma = f'{ma_new:8.4f}'
    mm = f'{mm_new:11.8f}'

    # Reconstruct TLE string
    out = line_num + ' ' + sat_num + ' ' + inclination + ' ' + \
          raan + ' ' + eccentricity + ' ' + ap + ' ' + \
          ma + ' ' + mm + rev_num

    # Add checksum
    out = add_check_sum(out)
    return out

def add_check_sum(out):
    # Add checksum
    check_sum = 0
    for a in out:
        if (a == '-'):
            check_sum = check_sum + 1
        if (a in '0123456789'):
            check_sum = check_sum + int(a)
    check_sum = check_sum % 10
    out = out + f'{check_sum}'
    return out

def vec2tle(vec,line1,line2):
    # Parse TLE lines
    (line_num1, sat_num1, launch_info, epoch_yr, epoch_day, mmd, mmdd, drag, eff_type, eset_num, check_sum1) = line1_to_param(line1)
    (line_num2, sat_num2, inclination, raan, eccentricity, ap, ma, mm, rev_num, check_sum2) = line2_to_param(line2)
    # Transfer over vector parameters
    inclination, raan, ap, mm = vec
    # inclination, raan, ap, ma, mm = vec
    # inclination, raan, ap, ma, epoch_day = vec
    # Reconstruct TLE lines
    line1 = build_line1(line_num1, sat_num1, launch_info, epoch_yr, epoch_day, mmd, mmdd, drag, eff_type, eset_num)
    line2 = build_line2(line_num2, sat_num2, inclination, raan, eccentricity, ap, ma, mm, rev_num)
    return line1, line2

def elements2tle(elements,line1,line2):
    # Parse TLE lines
    (line_num1, sat_num1, launch_info, epoch_yr, epoch_day, mmd, mmdd, drag, eff_type, eset_num, check_sum1) = line1_to_param(line1)
    (line_num2, sat_num2, inclination, raan, eccentricity, ap, ma, mm, rev_num, check_sum2) = line2_to_param(line2)
    # Transfer over vector parameters
    inclination, raan, eccentricity, ap, ma, mm = elements
    # Reconstruct TLE lines
    line1 = build_line1(line_num1, sat_num1, launch_info, epoch_yr, epoch_day, mmd, mmdd, drag, eff_type, eset_num)
    line2 = build_line2(line_num2, sat_num2, inclination, raan, eccentricity, ap, ma, mm, rev_num)
    return line1, line2

# Perturb TLE function
def perturb(line):
    (line_num, sat_num, inclination, raan, eccentricity, ap, ma, mm, rev_num, check_sum) = line2_to_param(line)

    # Generate random perturbation
    num = 2
    #params = [1, 1, 0.1, 1, 1]
    #diff = [0] * num
    params = [1] * num
    diff = [0] * num
    if(random() < 0.1): # 20% of the time randomize only one element
        i = randrange(num)
        diff[i] = uniform(-params[i],params[i])
        #if(i==2):
        #    diff[i] = diff[i] * eccentricity # multiplicative effect
    else:
        diff = [uniform(-p,p) for p in params]
        #diff[2] = diff[2] * eccentricity # multiplicative effect

    # Perturb TLE
    inclination_new = inclination + diff[0]
    raan_new = raan + diff[1]
    eccentricity_new = eccentricity # + diff[2]
    ap_new = ap # + diff[2]
    ma_new = ma # + diff[3]
    #ap_new = ap + diff[3]
    #ma_new = ma + diff[4]
    mm_new = mm + 0

    out = build_line2(line_num, sat_num, inclination_new, raan_new, eccentricity_new, ap_new, ma_new, mm_new, rev_num)

    return out, diff
