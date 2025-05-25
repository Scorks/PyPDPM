import os
import sys
import json
from itertools import product

# sys.path.append('..')

script_dir = os.path.dirname(__file__)

mapping_clinical_category = json.load(open(os.path.join(script_dir, 'data\\PDPM_ICD10_Mappings_FY2020_clinical_category.json')))
mapping_NTA = json.load(open(os.path.join(script_dir, 'data\\PDPM_ICD10_Mappings_FY2020_NTA.json')))
mapping_SLP = json.load(open(os.path.join(script_dir, 'data\\PDPM_ICD10_Mappings_FY2020_SLP.json')))


PAYMENT_GROUP_TO_HIPPS_CODE_VALUE = {('TA', 'SA', 'ES3', 'NA'): 'A', ('TB', 'SB', 'ES2', 'NB'): 'B',
                                     ('TC', 'SC', 'ES1', 'NC'): 'C', ('TD', 'SD', 'HDE2', 'ND'): 'D',
                                     ('TE', 'SE', 'HDE1', 'NE'): 'E', ('TF', 'SF', 'HBC2', 'NF'): 'F',
                                     ('TG', 'SG', 'CBC2'): 'G', ('TH', 'SH', 'CA2'): 'H',
                                     ('TI', 'SI', 'CBC1'): 'I', ('TJ', 'SJ', 'CA1'): 'J',
                                     ('TK', 'SK', 'BAB2'): 'K', ('TL', 'SL', 'BAB1'): 'L',
                                     ('TM', 'HBC1'): 'M', ('TN', 'LDE2'): 'N', ('TO', 'LDE1'): 'O',
                                     ('TP', 'LBC2'): 'P', ('LBC1'): 'Q', ('CDE2'): 'R', ('CDE1'): 'S',
                                     ('PDE2'): 'T', ('PDE1'): 'U', ('PBC2'): 'V', ('PA2'): 'W',
                                     ('PBC1'): 'X', ('PA1'): 'Y'}

VALID_PT_OT_GROUPS = ['TA', 'TB', 'TC', 'TD', 'TE', 'TF', 'TG', 'TH', 'TI', 'TJ', 'TK', 'TL', 'TM', 'TN', 'TO', 'TP']

VALID_SLP_GROUPS = ['SA', 'SB', 'SC', 'SD', 'SE', 'SF', 'SG', 'SH', 'SI', 'SJ', 'SK', 'SL']

VALID_NURS_GROUPS = ['ES3', 'ES2', 'ES1', 'HDE2', 'HDE1', 'HBC2', 'CBC2', 'CA2', 'CBC1', 'CA1', 'BAB2', 'BAB1', 'HBC1', 'LDE2', 'LDE1', 'LBC2', 'LBC1', 'CDE2', 'CDE1', 'PDE2', 'PDE1', 'PBC2', 'PA2', 'PBC1', 'PA1']

VALID_NTA_GROUPS = ['NA', 'NB', 'NC', 'ND', 'NE', 'NF']

VALID_AT_GROUPS = [0, 1, 6]

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

VARIABLE_PER_DIEM_ADJUSTMENTS = {'PT_OT': {range(1, 21): 1.00, range(21, 28): 0.98, range(28, 35): 0.96, range(
    35, 42): 0.94, range(42, 49): 0.92, range(49, 56): 0.90, range(56, 63): 0.88, range(63, 70): 0.86,
    range(70, 77): 0.84, range(77, 84): 0.82, range(84, 91): 0.80, range(91, 98): 0.78, range(98, 151): 0.76},
    'NTA': {range(1, 4): 3.00, range(4, 151): 1.00}}

def generateAllCodes():
    """
    
    Returns a list of all PDPM codes

    Returns
    ----------
    uniqueCodeList : list
        All possible codes that a patient could hold

    """
    uniqueCodeList = []
    codeCombinations = list(product(VALID_PT_OT_GROUPS, VALID_SLP_GROUPS, VALID_NURS_GROUPS, VALID_NTA_GROUPS))
    for code in codeCombinations:
        currentCode = ''
        for _ in range(len(code)):
            for key, value in PAYMENT_GROUP_TO_HIPPS_CODE_VALUE.items():
                if code[_] in key:
                    currentCode += value
        uniqueCodeList.append(currentCode)
    return uniqueCodeList

def getIntensityGroup(HIPPScode: str):
    """

    Groups a PDPM HIPPS code into one of ___ categories of care intensity

    Parameters
    ----------
    HIPPScode : str
        The PDPM HIPPS code for the patient

    """
    def normalize_dict_values(input_dict, new_min=0, new_max=10):
        """
        
        Normalizes a CMI dictionary between new_min and new_max for intensity scoring
        
        """
        # Find the minimum and maximum values in the dictionary
        min_value = min(input_dict.values())
        max_value = max(input_dict.values())

        # Normalize each value in the dictionary to the new range
        normalized_dict = {
            key: ((value - min_value) / (max_value - min_value)) * (new_max - new_min) + new_min
            for key, value in input_dict.items()
        }

        return normalized_dict
    
    def normalize_dict_of_tuples(input_dict, new_min=0, new_max=10):
        """
    
        Normalizes a CMI dictionary between new_min and new_max for intensity scoring (when values are tuples)

        
        """
        # Transpose the values to get separate lists for each element of the tuples
        transposed_values = list(zip(*input_dict.values()))

        # Normalize each list independently
        normalized_lists = [
            [((value - min(lst)) / (max(lst) - min(lst))) * (new_max - new_min) + new_min for value in lst]
            for lst in transposed_values
        ]

        # Transpose the normalized values back to tuples
        normalized_tuples = list(zip(*normalized_lists))

        # Create a new dictionary with the same keys and the normalized tuples
        normalized_dict = dict(zip(input_dict.keys(), normalized_tuples))

        return normalized_dict
    
    HIPPS_characters = [char for char in HIPPScode]
    PT_OT = HIPPS_characters[0]  # physical therapy and occupational therapy
    SLP = HIPPS_characters[1]  # speech-language pathology
    NPG = HIPPS_characters[2]  # nursing payment group
    NTA = HIPPS_characters[3]  # non-therapy ancillaries

    therapy_relative_significance_weights = {'PT': 0.186, 'OT': 0.174, 'SLP': 0.07, 'NPG': 0.325, 'NTA': 0.245}

    # normalize each CMI dictionary between 0 and 10
    PT_COMPONENT = normalize_dict_of_tuples(PT_OT_CMI_MAP, 0, 100)[PT_OT][0] * therapy_relative_significance_weights['PT']
    OT_COMPONENT = normalize_dict_of_tuples(PT_OT_CMI_MAP, 0, 100)[PT_OT][1] * therapy_relative_significance_weights['OT']
    SLP_COMPONENT = normalize_dict_values(SLP_CMI_MAP, 0, 100)[SLP] * therapy_relative_significance_weights['SLP']
    NPG_COMPONENT = normalize_dict_values(NPG_CMI_MAP, 0, 100)[NPG] * therapy_relative_significance_weights['NPG']
    NTA_COMPONENT = normalize_dict_values(NPG_CMI_MAP, 0, 100)[NTA] * therapy_relative_significance_weights['NTA']

    # return grouping between 0 and 100
    return round(PT_COMPONENT + OT_COMPONENT + SLP_COMPONENT + NPG_COMPONENT + NTA_COMPONENT)


def getReimbursementAmount(HIPPScode: str, dayOfStay: int, urban: bool = True, year: str = '2022') -> float:
    """

    Calculates the reimbursement for a specific day of a patient's stay.

    Parameters
    ----------
    HIPPScode : str
        The PDPM HIPPS code for the patient
    dayOfStay : int
        The day of the stay in which the reimbursement is being calculated for
    urban : bool
        Whether or not the facility is urban (default is True)
    year : str
        The year the reimbursement value is being calculated for (default is '2022')

    Returns
    -------
    float
        The amount (in dollars) that is reimbursed to the facility for one particular day

    """

    HIPPS_characters = [char for char in HIPPScode]
    PT_OT = HIPPS_characters[0]  # physical therapy and occupational therapy
    SLP = HIPPS_characters[1]  # speech-language pathology
    NPG = HIPPS_characters[2]  # nursing payment group
    NTA = HIPPS_characters[3]  # non-therapy ancillaries
    if (len(HIPPS_characters) >= 5):
        AT = HIPPS_characters[4]  # assessment type (0 or 1)
    else:
        AT = '0'

    try:
        PT_OT_CMI = PT_OT_CMI_MAP[PT_OT]
        SLP_CMI = SLP_CMI_MAP[SLP]
        NPG_CMI = NPG_CMI_MAP[NPG]
        NTA_CMI = NTA_CMI_MAP[NTA]
    except:
        raise Exception('Invalid HIPPS code')
    if urban:
        BASE_RATE_MAP = BASE_RATES_URBAN[year]
    else:
        BASE_RATE_MAP = BASE_RATES_RURAL[year]

    a = (next(VARIABLE_PER_DIEM_ADJUSTMENTS['PT_OT'][key]
         for key in VARIABLE_PER_DIEM_ADJUSTMENTS['PT_OT'] if 42 in key))

    try:
        reimbursement = round((PT_OT_CMI[0] * BASE_RATE_MAP['PT'] * (next(VARIABLE_PER_DIEM_ADJUSTMENTS['PT_OT'][key]
                                                                          for key in VARIABLE_PER_DIEM_ADJUSTMENTS['PT_OT'] if dayOfStay in key))) + (PT_OT_CMI[1] * BASE_RATE_MAP['OT']
                                                                                                                                                      * (next(VARIABLE_PER_DIEM_ADJUSTMENTS['PT_OT'][key]
                                                                                                                                                              for key in VARIABLE_PER_DIEM_ADJUSTMENTS['PT_OT'] if dayOfStay in key))) + (SLP_CMI * BASE_RATE_MAP['SLP']) + (NPG_CMI * BASE_RATE_MAP['NPG']) + (NTA_CMI * BASE_RATE_MAP['NTA'] * ((next(VARIABLE_PER_DIEM_ADJUSTMENTS['NTA'][key]
                                                                                                                                                                                                                                                                                                                                                        for key in VARIABLE_PER_DIEM_ADJUSTMENTS['NTA'] if dayOfStay in key)))), 2)
    except:
        raise Exception('Invalid arguments')
    else:
        return reimbursement
    
def calculateTotalReimbursement(HIPPScode: str, lengthOfStay: int, urban: bool = True, year: str = '2022') -> float:
    """

    Calculates the reimbursement for a specific day of a patient's stay.

    Parameters
    ----------
    HIPPScode : str
        The PDPM HIPPS code for the patient
    dayOfStay : int
        The current day of the stay
    urban : bool
        Whether or not the facility is urban (default is True)
    year : str
        The year the reimbursement value is being calculated for (default is '2022')

    Returns
    -------
    float
        The amount (in dollars) that is reimbursed to the facility from day 0 to day lengthOfStay

    """
    
    totalReimbursement = 0
    for day in range(1, lengthOfStay+1):
        totalReimbursement += getReimbursementAmount(HIPPScode, day, urban, year)
    return round(totalReimbursement, 2)

# generate HIPPS code -------------------------------------------------------------------------------------------------------------------------

# for the PT & OT components, two classifications are used (clinical category and functional status)

def _get_PT_OT_ClinicalCategory(ICD10CM_Code: str) -> str:
    """
    
    Convert ICD10CM_Code to PDPM Clinical Category using PDPM_ICD10_Mappings_FY2020_clinical_category, and then convert to PT & OT Clinical Categories.

    Parameters
    ----------
    ICD10CM_Code : str
        The PDPM HIPPS code for the patient

    Returns
    -------
    str
        The clinical category of the primary diagnosis

    """

    ICD10CM_Code = ICD10CM_Code.replace('.', '').strip()

    if ICD10CM_Code in mapping_clinical_category:
        PDPM_clinical_category = mapping_clinical_category[ICD10CM_Code]
        if PDPM_clinical_category in ['Acute Infections', 'Medical Management', 'Cancer', 'Pulmonary', 'Cardiovascular and Coagulations']:
            return 'Medical Management'
        elif PDPM_clinical_category in ['Non-Surgical Orthopedic/Musculoskeletal', 'Orthopedic Surgery (Except Major Joint Replacement or Spinal Surgery)']:
            return 'Other Orthopedic'
        elif PDPM_clinical_category in ['Acute Neurologic', 'Non-Orthopedic Surgery']:
            return 'Non-Orthopedic Surgery and Acute Neurologic'
        elif PDPM_clinical_category in ['Major Joint Replacement or Spinal Surgery']:
            return 'Major Joint Replacement or Spinal Surgery'
        
        # Return to provider: This indicates that the SNF will not receive payment. In such cases, one should wait for a correction or more information from the provider.
        elif PDPM_clinical_category == 'Return to Provider':
            return 'Return to Provider'
    else:
        return 'Unmapped'

def _get_PT_OT_ClinicalClassificationGroup(ICD10CM_Code: str, section_GG_function_score: int) -> str:
    """
    
    Convert ICD10CM_Code along with section GG function score to a clinical classification payment group

    Parameters
    ----------
    ICD10CM_Code : str
        The PDPM HIPPS code for the patient

    section_GG_function_score : int
        The section GG functional range score (standardized tool that measures the functional status and goals of the resident in various areas, including self-care, mobility, and communication)

    Returns
    -------
    str
        The clinical classification group of a patient

    Raises
    ------
    ValueError
        If the section_GG_function_score is less than 0 or greater than 24

    """

    '''
    GG0130A1 (Self-care: Eating) : 0 - 4
    GG0130B1 (Self-care: Oral Hygiene) : 0 - 4
    GG0130C1 (Self-care: Toileting Hygiene) : 0 - 4
    --------------------------------------------------
    GG0170B1 (Mobility: Sit to Lying) and GG0170C1 (Mobility: Lying to Sitting on side of bed) : 0 - 4 (average of two items)
    --------------------------------------------------
    GG0170D1 (Mobility: Sit to Stand) and GG0170E1 - Mobility: Chair/bed-to-chair transfer and GG0170F1 - Mobility: Toilet Transfer: 0 - 4 (average of 3 items)
    --------------------------------------------------
    GG0170J1 - Mobility: Walk 50 feet with 2 turns and GG0170K1 - Mobility: Walk 150 feet 0 - 4 (average of 2 items)

    The above values are summed, totaling to section_GG_function_score
    '''

    PT_OT_clinical_category = _get_PT_OT_ClinicalCategory(ICD10CM_Code)
    if (0 > int(section_GG_function_score) > 24):
        raise ValueError('Invalid section_GG_function_score, value must be an integer between 0 and 24')

    if PT_OT_clinical_category == 'Major Joint Replacement or Spinal Surgery':
        if section_GG_function_score in range(0, 6):
            return 'TA'
        elif section_GG_function_score in range(6, 10):
            return 'TB'
        elif section_GG_function_score in range(10, 24):
            return 'TC'
        elif section_GG_function_score == 24:
            return 'TD'
    elif PT_OT_clinical_category == 'Other Orthopedic':
        if section_GG_function_score in range(0, 6):
            return 'TE'
        elif section_GG_function_score in range(6, 10):
            return 'TF'
        elif section_GG_function_score in range(10, 24):
            return 'TG'
        elif section_GG_function_score == 24:
            return 'TH'
    elif PT_OT_clinical_category == 'Medical Management':
        if section_GG_function_score in range(0, 6):
            return 'TI'
        elif section_GG_function_score in range(6, 10):
            return 'TJ'
        elif section_GG_function_score in range(10, 24):
            return 'TK'
        elif section_GG_function_score == 24:
            return 'TL'
    elif PT_OT_clinical_category == 'Non-Orthopedic Surgery and Acute Neurologic':
        if section_GG_function_score in range(0,6):
            return 'TM'
        elif section_GG_function_score in range(6, 10):
            return 'TN'
        elif section_GG_function_score in range(10, 24):
            return 'TO'
        elif section_GG_function_score == 24:
            return 'TP'
    elif PT_OT_clinical_category == 'Return to Provider':
        return 'Return to Provider'
    elif PT_OT_clinical_category == 'Unmapped':
        return 'Unmapped'

def _get_SLP_CaseMixClassificationGroup(cognitiveImpairment: bool, acuteNeurologicalCondition: bool, mechanicallyAlteredDiet: bool, swallowingDisorder: bool, ICD10CM_Codes: list) -> str:
    """

    Convert comorbidity ICD-10-CM codes along with cognitive impairment status, acute neurological condition status, mechanically altered diet status, and swallowing disorder status to SLP (speech-language pathology) payment group

    Parameters
    ----------
    ICD10CM_Code : list
        List of ICD-10-CM does that are potential comorbidities

    cognitiveImpairment : bool
        Boolean value representing whether a patient has cognitive impairment

    acuteNeurologicalCondition : bool
        Boolean value representing whether a patient has an acute neurological condition

    mechanicallyAlteredDiet : bool
        Boolean value representing whether a patient has a mechanically altered diet

    swallowingDisorder : bool
        Boolean value representing whether a patient has a swallowing disorder


    Returns
    -------
    str
        The SLP payment group of a patient

    """

    for comorbidity in ICD10CM_Codes:
        if comorbidity.replace('.', '').strip() in mapping_SLP:
            comorbidityFlag = True
        else:
            comorbidityFlag = False
    
    if comorbidityFlag + cognitiveImpairment + acuteNeurologicalCondition == 0:
        if not mechanicallyAlteredDiet and not swallowingDisorder:
            return 'SA'
        elif (mechanicallyAlteredDiet + swallowingDisorder == 1):
            return 'SB'
        elif (mechanicallyAlteredDiet and swallowingDisorder):
            return 'SC'
    elif comorbidityFlag + cognitiveImpairment + acuteNeurologicalCondition == 1:
        if not mechanicallyAlteredDiet and not swallowingDisorder:
            return 'SD'
        elif (mechanicallyAlteredDiet + swallowingDisorder == 1):
            return 'SE'
        elif (mechanicallyAlteredDiet and swallowingDisorder):
            return 'SF'
    elif comorbidityFlag + cognitiveImpairment + acuteNeurologicalCondition == 2:
        if not mechanicallyAlteredDiet and not swallowingDisorder:
            return 'SG'
        elif (mechanicallyAlteredDiet + swallowingDisorder == 1):
            return 'SH'
        elif (mechanicallyAlteredDiet and swallowingDisorder):
            return 'SI'
    elif comorbidityFlag + cognitiveImpairment + acuteNeurologicalCondition == 3:
        if not mechanicallyAlteredDiet and not swallowingDisorder:
            return 'SJ'
        elif (mechanicallyAlteredDiet + swallowingDisorder == 1):
            return 'SK'
        elif (mechanicallyAlteredDiet and swallowingDisorder):
            return 'SL'
        
def _get_NURS_PaymentGroup(nursingPaymentGroup: str) -> str:
    '''
    Getting the Nursing Payment Group (NPG)

    Parameters
    ----------
    nursingPaymentGroup : str
        The CMG for a particular patient
    
    Returns
    -------
    str
        The nursing payment group if it is valid
    
    Raises
    ------
    ValueError
        If the nursingPaymentGroup is invalid
    '''

    if (nursingPaymentGroup in VALID_NURS_GROUPS):
        return nursingPaymentGroup
    else:
        raise ValueError('Invalid nursing payment group')

def _get_NTA_PaymentGroup(ICD10CM_Codes: list) -> str:
    '''
    Getting the Non-Therapy Ancillary (NTA) payment group

    Parameters
    ----------
    ICD10CM_Codes : list
        list of secondary diagnoses associated with a patient
    
    Returns
    -------
    str
        The NTA payment group
    
    '''
        
    NTA_score = 0
    for item in ICD10CM_Codes:
        if item in mapping_NTA:
            value = mapping_NTA[item]
            if value == 'HIV/AIDS':
                NTA_score += 8
            elif value == 'Major Organ Transplant Status, Except Lung':
                NTA_score += 2
            elif value == 'Lung Transplant Status':
                NTA_score += 3
            elif value == 'Opportunistic Infections':
                NTA_score += 2
            elif value == 'Aseptic Necrosis of Bone':
                NTA_score += 2
            elif value == 'Bone/Joint/Muscle Infections/Necrosis - Except : RxCC80: Aseptic Necrosis of Bone':
                NTA_score += 2
            elif value == 'Chronic Myeloid Leukemia':
                NTA_score += 2
            elif value == 'Endocarditis':
                NTA_score += 1
            elif value == 'Immune Disorders':
                NTA_score += 1
            elif value == 'End-Stage Liver Disease':
                NTA_score += 1
            elif value == 'Narcolepsy and Cataplexy':
                NTA_score += 1
            elif value == 'Cystic Fibrosis':
                NTA_score += 1
            elif value == 'Specified Hereditary Metabolic/Immune Disorders':
                NTA_score += 1
            elif value == 'Morbid Obesity':
                NTA_score += 1
            elif value == 'Psoriatic Arthropathy and Systemic Sclerosis':
                NTA_score += 1
            elif value == 'Chronic Pancreatitis':
                NTA_score += 1
            elif value == 'Proliferative Diabetic Retinopathy and Vitreous Hemorrhage':
                NTA_score += 1
            elif value == 'Complications of Specified Implanted Device or Graft':
                NTA_score += 1
            elif value == 'Aseptic Necrosis of Bone':
                NTA_score += 1
            elif value == 'Cardio-Respiratory Failure and Shock':
                NTA_score +=1
            elif value == 'Myelodysplastic Syndromes and Myelofibrosis':
                NTA_score += 1
            elif value == 'Systemic Lupus Erythematosus, Other Connective Tissue Disorders, and Inflammatory Spondylopathies':
                NTA_score += 1
            elif value == 'Diabetic Retinopathy - Except : CC122: Proliferative Diabetic Retinopathy and Vitreous Hemorrhage':
                NTA_score += 1
            elif value == 'Severe Skin Burn or Condition':
                NTA_score += 1
            elif value == 'Intractable Epilepsy':
                NTA_score += 1
            elif value == 'Disorders of Immunity - Except : RxCC97: Immune Disorders':
                NTA_score += 1
            elif value == 'Cirrhosis of Liver':
                NTA_score += 1
            elif value == 'Respiratory Arrest':
                NTA_score +=1
            elif value == 'Pulmonary Fibrosis and Other Chronic Lung Disorders':
                NTA_score += 1
    
    if NTA_score in range(0, 1):
        return 'NF'
    elif NTA_score in range(1, 3):
        return 'NE'
    elif NTA_score in range(3, 6):
        return 'ND'
    elif NTA_score in range(6, 9):
        return 'NC'
    elif NTA_score in range(9, 12):
        return 'NB'
    else:
        return 'NA'

def _get_AssessmentIndicator(assessmentType: str) -> str:
    '''
    Getting the assessment indicator (AI)

    Parameters
    ----------
    assessmentType : str
        'IPA', 'PPS 5-day', or 'OBRA' representing the assessment type
    
    Returns
    -------
    str
        The assessment indicator (0, 1, 6, or '-' if assessmentType is invalid)
    
    '''
    
    if assessmentType == 'IPA':
        return '0'
    elif assessmentType == 'PPS 5-day':
        return '1'
    elif assessmentType == 'OBRA': # Omnibus Budget Reconciliation Act - not coded as a PPS Assessment
        return '6'
    else:
        return '-'
    
def get_PDPM_HIPPS_code(ICD10CM_primaryDiagnosisCode: str, section_GG_function_score: int, cognitiveImpairment: bool, acuteNeurologicalCondition: bool, mechanicallyAlteredDiet: bool, swallowingDisorder: bool, ICD10CM_SLP_Codes: list, ICD10CM_NTA_Codes: list, nursingPaymentGroup: str, assessmentType: str):
    '''
    Getting the PDPM HIPPS code for a patient given a set of patient information

    Parameters
    ----------
    ICD10CM_primaryDiagnosisCode : str
        Primary diagnosis of the patient

    section_GG_function_score : int
        The section GG functional range score (standardized tool that measures the functional status and goals of the resident in various areas, including self-care, mobility, and communication)

    ICD10CM_SLP_Codes : list
        List of ICD-10-CM does that are potential comorbidities

    cognitiveImpairment : bool
        Boolean value representing whether a patient has cognitive impairment

    acuteNeurologicalCondition : bool
        Boolean value representing whether a patient has an acute neurological condition

    mechanicallyAlteredDiet : bool
        Boolean value representing whether a patient has a mechanically altered diet

    swallowingDisorder : bool
        Boolean value representing whether a patient has a swallowing disorder

    ICD10CM_Codes : list
        list of secondary diagnoses associated with a patient for NTA payment group calculation

    nursingPaymentGroup : str
        The CMG for a particular patient

    assessmentType : str
        'IPA', 'PPS 5-day', or 'OBRA' representing the assessment type
    
    Returns
    -------
    str
        The PDPM HIPPS code of a patient
    
    '''
    PT_OT_PaymentGroup = _get_PT_OT_ClinicalClassificationGroup(ICD10CM_primaryDiagnosisCode, section_GG_function_score)
    if PT_OT_PaymentGroup == 'Return to provider' or PT_OT_PaymentGroup == 'Unmapped':
        raise ValueError('Invalid value for ICD10CM_primaryDiagnosisCode and or section_GG_function_score (0-24)')
    SLP_PaymentGroup = _get_SLP_CaseMixClassificationGroup(cognitiveImpairment, acuteNeurologicalCondition, mechanicallyAlteredDiet, swallowingDisorder, ICD10CM_SLP_Codes)
    NURS_PaymentGroup = _get_NURS_PaymentGroup(nursingPaymentGroup)
    NTA_PaymentGroup = _get_NTA_PaymentGroup(ICD10CM_NTA_Codes)
    assessmentIndicator = _get_AssessmentIndicator(assessmentType)
    HIPPS_code = get_PDPM_HIPPS_code(PT_OT_PaymentGroup, SLP_PaymentGroup, NURS_PaymentGroup, NTA_PaymentGroup, assessmentIndicator)
    return HIPPS_code

def get_PDPM_HIPPS_code(PT_OT_PaymentGroup: str, SLP_PaymentGroup: str, NURS_PaymentGroup: str, NTA_PaymentGroup: str, assessmentIndicator: int = 0) -> str:
    '''
    Getting the PDPM HIPPS code for a patient given the payment groups for a patient

    Parameters
    ----------
    PT_OT_PaymentGroup : str
        PT/OT payment group - one of: ('TA', 'TB', 'TC', 'TD', 'TE', 'TF', 'TG', 'TH', 'TI', 'TJ', 'TK', 'TL', 'TM', 'TN', 'TO', 'TP')

    SLP_PaymentGroup : str
        SLP payment group - one of: ('SA', 'SB', 'SC', 'SD', 'SE', 'SF', 'SG', 'SH', 'SI', 'SJ', 'SK', 'SL')

    NURS_PaymentGroup : str
        NURSING payment group - one of: ('ES3', 'ES2', 'ES1', 'HDE2', 'HDE1', 'HBC2', 'CBC2', 'CA2', 'CBC1', 'CA1', 'BAB2', 'BAB1', 'HBC1', 'LDE2', 'LDE1', 'LBC2', 'LBC1', 'CDE2', 'CDE1', 'PDE2', 'PDE1', 'PBC2', 'PA2', 'PBC1', 'PA1')

    NTA_PaymentGroup : str
        NTA payment group - one of: ('NA', 'NB', 'NC', 'ND', 'NE', 'NF')

    assessmentIndicator:
        assessment indicator value - one of (0, 1, 6) default is 0
    
    Returns
    -------
    str
        The PDPM HIPPS code of a patient
    
    '''
    if (PT_OT_PaymentGroup not in VALID_PT_OT_GROUPS):
        raise ValueError('Invalid value for PT_OT_PaymentGroup')
    elif (SLP_PaymentGroup not in VALID_SLP_GROUPS):
        raise ValueError('Invalid value for SLP_PaymentGroup')
    elif (NURS_PaymentGroup not in VALID_NURS_GROUPS):
        raise ValueError('Invalid value for NURS_PaymentGroup')
    elif (NTA_PaymentGroup not in VALID_NTA_GROUPS):
        raise ValueError('Invalid value for NTA_PaymentGroup')
    elif (assessmentIndicator not in VALID_AT_GROUPS):
        raise ValueError('Invalid value for assessmentIndicator')
    else:
        HIPPS_code = next(v for k, v in PAYMENT_GROUP_TO_HIPPS_CODE_VALUE.items() if PT_OT_PaymentGroup in k) + next(v for k, v in PAYMENT_GROUP_TO_HIPPS_CODE_VALUE.items() if SLP_PaymentGroup in k) + next(v for k, v in PAYMENT_GROUP_TO_HIPPS_CODE_VALUE.items() if NURS_PaymentGroup in k) + next(v for k, v in PAYMENT_GROUP_TO_HIPPS_CODE_VALUE.items() if NTA_PaymentGroup in k) + str(assessmentIndicator)
    
    return HIPPS_code

'''
code = get_PDPM_HIPPS_code('TD', 'SG', 'CBC1', 'NE', 1)
code = 'CLAA1'
print(getIntensityGroup(code))

def test() -> int:
    return 1

fileReader = open('ICDCODES.txt', 'r')

myDict = {}

lines = fileReader.readlines()
for line in lines:
    line = line.split()
    arg = line[1]
    response = (_get_PT_OT_ClinicalCategory(arg))
    if response in myDict:
        myDict[response] += 1
    else:
        myDict[response] = 0

print(myDict)

# print(_get_PT_OT_ClinicalCategory('S72399H      '))
#print(_get_PT_OT_ClinicalClassificationGroup('T82510A        ', 10))
# print(_get_SLP_CaseMixClassificationGroup(True, True, False, True, ['I69991', 'C322', 'notACode']))

code = get_PDPM_HIPPS_code('TC', 'SC', 'PA1', 'NA', 0)
code = get_PDPM_HIPPS_code('TC', 'SC', 'PA1', 'NA')
print(code)
print(getReimbursementAmount(code, 4))
print(calculateTotalReimbursement(code, 30))
'''