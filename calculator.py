import math

import Satellite as satellite

import Satellite


# done
def convert_TPC_to_time_from_start_GPS_week(Tpc, Toe):
    return (int(Toe / 86400) * 86400 + Tpc.hour * 3600 + Tpc.minute * 60 + Tpc.second)


# done
def calculate_t_k(t, t_oe):
    t_k = t - t_oe
    if t_k > 302400:
        t_k -= 604800
    if t_k < -302400:
        t_k += 604800
    return t_k


# done
def corrected_average_movement(delta_n, a):
    n = math.sqrt((3.986005 * math.pow(10, 14)) / math.pow(a, 3)) + delta_n
    return n


# done
def current_average_anomaly(m0, n, t_k):
    return m0 + n * t_k


# done
def eccentric_anomaly_EK(m_k, e0):
    ekn = m_k
    while True:
        ek = ekn
        ekn = m_k - ek + e0 * math.sin(ek)
        ekn = ekn / (1 - e0 * math.cos(ek))
        ekn += ek
        if abs(ekn - ek) < 0.0001:
            break
    return ek


# done
def derivativeEk(ekn, n, e0):
    return n / (1 - e0 * math.cos(ekn))


# done
def true_anomaly(ek, e0):
    res = math.sqrt(1 - math.pow(e0, 2)) * math.sin(ek)
    res /= (math.cos(ek) - e0)
    return math.atan(res)

# done
def latitude_argument(anomaly, w):
    return anomaly + w

# done
def derivative_latitude_argument(e0, devek, ek):
    res = math.sqrt(1 - math.pow(e0, 2)) * devek
    res /= (1 - e0 * math.cos(ek))
    return res

# done
def corrected_latitude_argument(fk, cuc, cus):
    deltaU = cuc * math.cos(2 * fk) + cus * math.sin(2 * fk)
    return fk + deltaU

# done
def derivative_corrected_latitude_argument(devFk, cuc, cus, fk):
    return devFk * (1 + 2 * (cuc * math.cos(2 * fk) - cus * math.sin(2 * fk)))

# done
def corrected_radius_vector(A, e0, ek, crc, crs, fk):
    deltaRk = crc * math.cos(2 * fk) + crs * math.sin(2 * fk)
    return A * (1 - e0 * math.cos(ek)) + deltaRk

# done
def derivative_radius_vector(A, e0, devEk, Ek, devFk, Fk, Crc, Crs):
    res = A * e0 * devEk * math.sin(Ek)
    res += 2 * devFk * (Crc * math.cos(2 * Fk) + Crs * math.sin(2 * Fk))
    return res

# done
def corrected_orbit_tilt_angle(I0, IDOT, tk, Cic, Cis, Fk):
    deltaIk = Cic * math.cos(2 * Fk) + Cis * math.sin(2 * Fk)
    return I0 + deltaIk + IDOT * tk

# done
def derivative_corrected_orbit_tilt_angle(IDOT, devFk, Cis, Cic, Fk):
    return IDOT + 2 * devFk * (Cis * math.cos(2 * Fk) + Cic * math.sin(2 * Fk))

# done
def vector_satellites_location(rk, uk):
    vector = [0, 0]
    vector[0] = rk * math.cos(uk)
    vector[1] = rk * math.sin(uk)
    return vector

# done
def derivative_vector_location(vectorLocation, devRk, Uk, devUk):
    vector = [0, 0]
    vector[0] = devRk * math.cos(Uk) - vectorLocation[1] * devUk
    vector[1] = devRk * math.sin(Uk) - vectorLocation[0] * devUk
    return vector

# done
def corrected_longitude_ascending_node(omegaO, OMEGADOT, tk, toe):
    w3 = 7.2921151467 * math.pow(10, -5)
    return omegaO + (OMEGADOT - w3) * tk - w3 * toe

# done
def derivative_longitude_ascending_node(OMEGADOT):
    w3 = 7.2921151467 * math.pow(10, -5)
    return OMEGADOT - w3

# done
def coordinates_at_tk(vectorLocation, omegaK, Ik):
    coord = [0, 0, 0]
    coord[0] = (vectorLocation[0] * math.cos(omegaK) - vectorLocation[1] * math.cos(Ik) * math.sin(omegaK)) / 1000
    coord[1] = (vectorLocation[0] * math.sin(omegaK) + vectorLocation[1] * math.cos(Ik) * math.cos(omegaK)) / 1000
    coord[2] = vectorLocation[1] * math.sin(Ik) / 1000
    return coord

# done
def speed_vector(coord, devOmegaK, vectorLocation, devVectorLocation, omegaK, Ik, devIk):
    speed = [0, 0, 0]
    speed[0] = -devOmegaK * coord[1] + devVectorLocation[0] * math.cos(omegaK) - (
            devVectorLocation[1] * math.cos(Ik) - vectorLocation[1] * devIk * math.sin(Ik)) * math.sin(omegaK)
    speed[1] = devOmegaK * coord[0] + devVectorLocation[0] * math.sin(omegaK) + (
            devVectorLocation[1] * math.cos(Ik) - vectorLocation[1] * devIk * math.sin(Ik)) * math.cos(omegaK)
    speed[2] = vectorLocation[1] * devIk * math.sin(Ik) + devVectorLocation[1] * math.sin(Ik)
    return speed


def calculateSpeeds(orbit: satellite):
    t = convert_TPC_to_time_from_start_GPS_week(orbit.TOC, orbit.tOE)
    tk = calculate_t_k(t, orbit.tOE)
    n = corrected_average_movement(orbit.deltaN, math.pow(orbit.sqrtA, 2))
    mk = current_average_anomaly(orbit.M0, n, tk)
    ek = eccentric_anomaly_EK(mk, orbit.e0)
    dev_ek = derivativeEk(ek, n, orbit.e0)
    teta_k = true_anomaly(ek, orbit.e0)
    fk = latitude_argument(teta_k, orbit.w)
    dev_fk = derivative_latitude_argument(orbit.e0, dev_ek, ek)
    uk = corrected_latitude_argument(fk, orbit.CUC, orbit.CUS)
    dev_uk = derivative_corrected_latitude_argument(dev_fk, orbit.CUC, orbit.CUS, fk)
    rk = corrected_radius_vector(math.pow(orbit.sqrtA, 2), orbit.e0, ek, orbit.CRC, orbit.CRS, fk)
    dev_rk = derivative_radius_vector(math.pow(orbit.sqrtA, 2), orbit.e0, dev_ek, ek, dev_fk, fk, orbit.CRC, orbit.CRS)
    ik = corrected_orbit_tilt_angle(orbit.I0, orbit.IDOT, tk, orbit.CIC, orbit.CIS, fk)
    dev_ik = derivative_corrected_orbit_tilt_angle(orbit.IDOT, dev_fk, orbit.CIS, orbit.CIC, fk)
    vector_location = vector_satellites_location(rk, uk)
    dev_vector_location = derivative_vector_location(vector_location, dev_rk, uk, dev_uk)
    omega_k = corrected_longitude_ascending_node(orbit.omega0, orbit.OMEGADOT, tk, orbit.tOE)
    dev_omega_k = derivative_longitude_ascending_node(orbit.OMEGADOT)
    coord = coordinates_at_tk(vector_location, omega_k, ik)
    speed = speed_vector(coord, dev_omega_k, vector_location, dev_vector_location, omega_k, ik, dev_ik)
    res = []
    for i in range(0, len(coord)):
        res.append(coord[i])
    for i in range(0, len(speed)):
        res.append(speed[i])
    return res
