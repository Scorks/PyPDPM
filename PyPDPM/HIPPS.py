import bisect

PT_OT_CMI_MAP = {'A': [1.53, 1.49], 'B': [1.69, 1.63], 'C': [1.88, 1.68],
                 'D': [1.92, 1.53], 'E': [1.42, 1.41], 'F': [1.61, 1.59],
                 'G': [1.67, 1.64], 'H': [1.16, 1.15], 'I': [1.13, 1.17],
                 'J': [1.42, 1.44], 'K': [1.52, 1.54], 'L': [1.09, 1.11],
                 'M': [1.27, 1.30], 'N': [1.48, 1.49], 'O': [1.55, 1.55],
                 'P': [1.08, 1.09]}

SLP_CMI_MAP = {'A': 0.68, 'B': 1.82, 'C': 2.66, 'D': 1.46, 'E': 2.33, 'F': 2.97,
               'G': 2.04, 'H': 2.85, 'I': 3.51, 'J': 2.98, 'K': 3.69, 'L': 4.19}

NPG_CMI_MAP = {'A': 4.04, 'B': 3.06, 'C': 2.91, 'D': 2.39, 'E': 1.99, 'F': 2.23,
               'G': 1.85, 'H': 2.07, 'I': 1.72, 'J': 1.71, 'K': 1.43, 'L': 1.86,
               'M': 1.62, 'N': 1.54, 'O': 1.08, 'P': 1.34, 'Q': 0.94, 'R': 1.04,
               'S': 0.99, 'T': 1.57, 'U': 1.47, 'V': 1.21, 'W': 0.7, 'X': 1.13,
               'Y': 0.66}

NTA_CMI_MAP = {'A': 3.25, 'B': 2.53,
               'C': 1.85, 'D': 1.34, 'E': 0.96, 'F': 0.72}

AT_CMI_MAP = {}

BASE_RATES_URBAN = {'2022': {'PT': 62.84, 'OT': 58.49,
                             'SLP': 23.46, 'NPG': 109.55, 'NTA': 82.64, 'NCM': 98.10}}

BASE_RATES_RURAL = {'2022': {'PT': 71.63, 'OT': 65.79,
                             'SLP': 29.56, 'NPG': 104.66, 'NTA': 78.96, 'NCM': 99.91}}

PER_DIEM_ADJUSTMENTS = {'PT_OT': {range(1, 21): 1.00, range(21, 28): 0.98, range(28, 35): 0.96, range(
    35, 42): 0.94, range(42, 49): 0.92, range(49, 56): 0.90, range(56, 63): 0.88, range(63, 70): 0.86,
    range(70, 77): 0.84, range(77, 84): 0.82, range(84, 91): 0.80, range(91, 98): 0.78, range(98, 151): 0.76},
    'NTA': {range(1, 4): 3.00, range(4, 151): 1.00}}


def getReimbursementAmount(HIPPScode: str, dayOfStay: int, urban: bool = True, year: str = '2022') -> float:
    HIPPS_characters = [char for char in HIPPScode]
    PT_OT = HIPPS_characters[0]  # physical therapy and occupational therapy
    SLP = HIPPS_characters[1]  # speech-language pathology
    NPG = HIPPS_characters[2]  # nursing payment group
    NTA = HIPPS_characters[3]  # non-therapy ancillaries
    AT = HIPPS_characters[4]  # assessment type (0 or 1)

    try:
        PT_OT_CMI = PT_OT_CMI_MAP[PT_OT]
        SLP_CMI = SLP_CMI_MAP[SLP]
        NPG_CMI = NPG_CMI_MAP[NPG]
        NTA_CMI = NTA_CMI_MAP[NTA]
    except Exception:
        raise Exception('Invalid HIPPS code')
    if urban:
        BASE_RATE_MAP = BASE_RATES_URBAN[year]
    else:
        BASE_RATE_MAP = BASE_RATES_RURAL[year]

    a = (next(PER_DIEM_ADJUSTMENTS['PT_OT'][key]
         for key in PER_DIEM_ADJUSTMENTS['PT_OT'] if 42 in key))

    try:
        reimbursement = round((PT_OT_CMI[0] * BASE_RATE_MAP['PT'] * (next(PER_DIEM_ADJUSTMENTS['PT_OT'][key]
                                                                          for key in PER_DIEM_ADJUSTMENTS['PT_OT'] if dayOfStay in key))) + (PT_OT_CMI[1] * BASE_RATE_MAP['OT']
                                                                                                                                             * (next(PER_DIEM_ADJUSTMENTS['PT_OT'][key]
                                                                                                                                                     for key in PER_DIEM_ADJUSTMENTS['PT_OT'] if dayOfStay in key))) + (SLP_CMI * BASE_RATE_MAP['SLP']) + (NPG_CMI * BASE_RATE_MAP['NPG']) + (NTA_CMI * BASE_RATE_MAP['NTA'] * ((next(PER_DIEM_ADJUSTMENTS['NTA'][key]
                                                                                                                                                                                                                                                                                                                                      for key in PER_DIEM_ADJUSTMENTS['NTA'] if dayOfStay in key)))), 2)
    except:
        raise Exception('Invalid arguments')
    else:
        return reimbursement


'''
def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """
    Calculate the great circle distance between two points on the
    earth (specified in decimal degrees), returns the distance in
    meters.
    All arguments must be of equal length.
    :param lon1: longitude of first place
    :param lat1: latitude of first place
    :param lon2: longitude of second place
    :param lat2: latitude of second place
    :return: distance in meters between the two sets of coordinates
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r
'''


def test() -> int:
    return 1


print(getReimbursementAmount('ABCD1', 30))
