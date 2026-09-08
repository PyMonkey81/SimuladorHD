import os
import random
import sys
import serial
import serial.tools.list_ports
import threading
import struct
import crcmod
import time
from PySide6.QtWidgets import (QApplication, QCheckBox, QSpinBox, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QComboBox, QPushButton, QGroupBox,QGridLayout,
                               QDoubleSpinBox)
from PySide6.QtCore import QTimer
from PySide6.QtCore import Qt, Signal, Slot

#core/variables.py



from typing import Dict, List, Tuple, Any

# ================================================================
# MAPEO COMPLETO DE VARIABLES - HEMODIÁLISIS
# ================================================================

VARIABLES: Dict[int, Dict[int, Dict[str, Any]]] = {

    # ================================================================
    # BOOLEANOS OPERACIÓN (0x01) - 60 variables (0x00 a 0x3B)
    # ================================================================
    0x01: {
        **{i: {"name": name, "label": label,"type": "bool", "rw": True, "nivel": nivel, "tag": tag, "id": i}
            for i, (name, label, nivel, tag) in enumerate([
                # --- VARIABLES DE CONTROL (ESCRITURA/LECTURA) - ID 0 a 40 (RW=True) ---
                
                ("Bomba peristáltica - Arranque", "INICIAR B.S.", "cian", "bloodPumpStartButton"),      # 0
                ("Bomba peristáltica - Paro", "PARAR B.S.", "cian", "bloodPumpStopButton"),             # 1
                ("Bomba peristáltica - Avance", "FWD B.S.", "cian", "bloodPumpFWDButton"),              # 2
                ("Bomba peristáltica - Reversa", "BCK B.S.", "cian", "bloodPumpREVButton"),             # 3
                ("Bomba de purga - Arranque", "INICIAR PURGA", "cian", "dialyserPumpStartButton"),      # 4
                ("Bomba de purga - Paro", "PARAR PURGA", "cian", "dialyserPumpStopButton"),             # 5
                ("Bomba Heparina - Arranque", "INIC. HEPARINA", "cian", "heparinePumpsStartButton"),    # 6
                ("Bomba Heparina - Paro", "PARAR HEPARINA", "cian", "heparinePumpsStopButton"),         # 7
                ("Bomba Heparina - Avance", "FWD HEPARINA", "cian", "heparinePumpFWDButton"),           # 8
                ("Bomba Heparina - Reversa", "REV HEPARINA", "cian", "heparinePumpREVButton"),          # 9
                ("Control Flujo Sangre - Habilitar", "HAB. CTRL FLUJO", "cian", "bloodControlLoopEnable"), # 10
                ("Control Flujo Sangre - Auto/Manual", "AUTO/MAN FLUJO", "cian", "bloodControlLoopMode"),  # 11
                ("Control Conductividad - Habilitar", "HAB. CTRL COND", "cian", "dialyCondCtrlLoopEnable"),# 12
                ("Control Conductividad - Auto/Manual", "AUTO/MAN COND", "cian", "dialyCondCtrlLoopMode"), # 13
                ("Control Temp Dializante - Habilitar", "HAB. CTRL TEMP", "cian", "dialyTempCtrlLoopEnable"),# 14
                ("Control Temp Dializante - Auto/Manual", "AUTO/MAN TEMP", "cian", "dialyTempCtrlLoopMode"), # 15
                ("Bomba Heparina - Home", "HOME HEPARINA", "cian", "heparinePumpHomePosition"),         # 16
                ("Cámara Balance - Start", "INICIO CAM.BAL", "cian", "dialiserBalChambStrButt"),        # 17
                ("Cámara Balance - Stop", "PARO CAM.BAL", "cian", "dialiserBalChambStpButt"),           # 18
                ("Bolo Heparina", "BOLO HEPARINA", "cian", "heparinApplyBolusDose"),                    # 19
                ("Pausar/Continuar", "PAUSA/CONT.", "cian", "heparineOperPauseResume"),                 # 20
                ("Operar Elementos Dializante", "ELEM. DIALIZ.", "cian", "dialyCircuitElementsOpSel"),  # 21
                ("Bomba Purga Dializante - Start", "INI PURGA DIAL", "cian", "dialyPurgePumpStartButt"), # 22
                ("Bomba Purga Dializante - Stop", "FIN PURGA DIAL", "cian", "dialyPurgePumpStopButt"),   # 23
                ("Bomba UF - Start", "INICIAR UF", "cian", "dialyUltraFPumpStartButt"),                 # 24
                ("Bomba UF - Stop", "PARAR UF", "cian", "dialyUltraFPumpStoptButt"),                    # 25
                ("Bomba Bicarbonato - Start", "INI BICARBONATO", "cian", "dialyBicarbonPumpStartButt"), # 26
                ("Bomba Bicarbonato - Stop", "FIN BICARBONATO", "cian", "dialyBicarbonPumpStopButt"),   # 27
                ("Bomba Ácido Cítrico - Start", "INI AC.CITRICO", "cian", "dialyCitricAcPumpStartButt"),# 28
                ("Bomba Ácido Cítrico - Stop", "FIN AC.CITRICO", "cian", "dialyCitricAcPumpStopButt"),  # 29
                ("Válvula Agua Entrada", "VALV ENTRADA", "cian", "dialyWaterInletValveButt"),           # 30
                ("Válvula Recirculación", "VALV RECIRCUL", "cian", "dialyRecirculatValveButt"),         # 31
                ("Válvula Cámara Caliente", "VALV CAM.CAL.", "cian", "dialyHotChambValveButt"),         # 32
                ("Válvula Venteo Aire", "VALV VENTEO", "cian", "dialyAirVentSepChambButt"),             # 33
                ("Válvula Bypass Filtro", "VALV BYPASS", "cian", "dialyBypassFilterButt"),              # 34
                ("Válvula Corte Entrada Filtro", "CORTE ENT FILT", "cian", "dialyInputFilterCutButt"),  # 35
                ("Válvula Corte Salida Filtro", "CORTE SAL FILT", "cian", "dialyOutputFilterCutButt"),  # 36
                ("Válvula de Drenaje", "VALV DRENAJE", "cian", "dialyWaterDrainValveButt"),             # 37
                ("Fin de Ciclo Cámara Balance", "FIN CICLO BAL", "amarillo", "dialyBalanceChambCycleEnd"),# 38
                ("Iniciar Diálisis", "INICIO DIALISIS", "cian", "dialyStartDialysisButt"),              # 39
                ("Parar Diálisis", "PARO DIALISIS", "cian", "dialyStopDialysisButt"),                   # 40
                ("Protección Resistores Calefactor", "PROT CALEFACTOR", "cian", "watterTankHeaterProtect"), # 41     alarma que se activa constantemente pero no importante para usuario
                ("Disponible para Función Digital 3", "RESERVA 3", "cian", "availableBoolVariable1"),       # 42
                ("Disponible para Función Digital 4", "RESERVA 4", "cian", "availableBoolVariable2"),       # 43
                ("Disponible para Función Digital 5", "RESERVA 5", "cian", "availableBoolVariable3"),       # 44
                ("Disponible para Función Digital 6", "RESERVA 6", "cian", "availableBoolVariable4"),       # 45
                ("Disponible para Función Digital 7", "RESERVA 7", "cian", "availableBoolVariable5"),       # 46
                ("Disponible para Función Digital 8", "RESERVA 8", "cian", "availableBoolVariable6"),       # 47
                ("Detector Burbuja Aire en Sangre", "AIRE EN LINEA", "rojo", "airBubbleInBloodDetected"),   # 48 (ALARMA)
                ("Detector Sangre en Dializante", "FUGA SANGRE", "rojo", "bloodInDialyCircDetected"),       # 49 (ALARMA)
                ("Nivel Alto Tanque Agua", "NIVEL AGUA ALTO", "amarillo", "dialyTankHiLevelSwitch"),        # 50
                ("Nivel Cámara Deaereación", "NIVEL DEAERAC.", "amarillo", "dialyDeaerChamLevSwitch"),      # 51
                ("Disponible para Función Digital 11", "RESERVA 11", "cian", "availableBoolVariable7"),     # 52
                ("Start Operation mode", "ESTADO START", "cian", "dialyModeOperationStart"),                      # 53
                ("Stop Operation mode", "ESTADO STOP", "cian", "dialyModeOperationStop"),                         # 54
                ("Pause Operation mode", "ESTADO PAUSE", "cian", "dialyModeOperationPause"),    # 55
                ("Llenado de filtro", "LLENADO DE FILTRO", "cian", "dialyFilterFillButton"),    # 56
                ("Sobrepresión Bomba Diálisis", "SOBREPRESIÓN DIALIZANTE", "rojo", "dialyDialyPumpOverPress"),    # 57
                ("Sobrepresión Bomba Deaeración", "SOBREPRESIÓN DEAERACIÓN", "rojo", "dialyDeaerPumpOverPress"),    # 58
                ("Disponible para Función Digital 18", "RESERVA 18", "cian", "availableBoolVariable14"),    # 59
            ], start=0)}
    },


    # ================================================================
    # PARÁMETROS CLÍNICOS (0x02)
    # ================================================================
    0x02: {
        0x00: {"name": "Presión intermembrana", "label": "PTM", "type": "double", "rw": True, "unit": "mmHg", "limites": (1, 100), "tag": "interMembPresClinicData", "nivel": "cian"},           # 0
        0x01: {"name": "Selección de modo de tratamiento", "label": "MODO TTO", "type": "double", "rw": True, "unit": "NA", "limites": (0, 100), "tag": "treatmentModeSelection", "nivel": "cian"}, # 1
        0x02: {"name": "Estado actual de proceso de cebado", "label": "ESTADO CEBADO", "type": "double", "rw": True, "unit": "NA", "limites": (0, 100), "tag": "primingProcessStatus", "nivel": "cian"},  # 2
        0x03: {"name": "Variable clínica visualización 3", "label": "VAR CLINICA 3", "type": "double", "rw": True, "unit": "NA", "limites": (0, 100), "tag": "availableClinicVariable4", "nivel": "cian"},  # 3
        0x04: {"name": "Selector de ciclos cámara de balance", "label": "SET CICLOS BAL.", "type": "double", "rw": True, "unit": "n", "limites": (1, 100), "tag": "balanceChamberCycleSet", "nivel": "cian"}, # 4
        0x05: {"name": "Volumen de heparina dosificado actual", "label": "VOL. HEPARINA", "type": "double", "rw": True, "unit": "ml", "limites": (0, 100), "tag": "heparineCurrentDosage", "nivel": "cian"},# 5
        0x06: {"name": "Número de ciclos cámara de balance", "label": "CICLOS ACTUAL", "type": "double", "rw": True, "unit": "c", "limites": (0, 10000), "tag": "balanceChamberCycleCount", "nivel": "cian"},# 6
    },
    # ================================================================
    # SETPOINTS (0x03)
    # ================================================================
    0x03: {
        0x00: {"name": "Velocidad de UltraFiltrado", "label": "TASA UF", "type": "double", "rw": True, "unit": "L/h", "limites": (0, 2), "tag": "ultraFilterPumpSpeed", "nivel": "cian"},              # 7
        0x01: {"name": "Ajuste de tiempo de ciclo de cámara de balance", "label": "TIEMPO CICLO", "type": "double", "rw": True, "unit": "s", "limites": (0, 100), "tag": "balanceChamberSetTiming", "nivel": "cian"}, # 8
        0x02: {"name": "Tiempo terapia: horas", "label": "T. TTO (H)", "type": "double", "rw": True, "unit": "h", "limites": (0, 10), "tag": "heparineTherapyHours", "nivel": "cian"},                    # 9
        0x03: {"name": "Tiempo terapia: minutos", "label": "T. TTO (M)", "type": "double", "rw": True, "unit": "m", "limites": (0, 59), "tag": "heparineTherapyMinutes", "nivel": "cian"},               # 10
        0x04: {"name": "Tamaño de escala de jeringa", "label": "ESC. JERINGA", "type": "double", "rw": True, "unit": "mm/ml", "limites": (1, 10), "tag": "heparineSyrinjeScaleSize", "nivel": "cian"},      # 11
        0x05: {"name": "Dosis de heparina por terapia ml/h", "label": "DOSIS HEPAR", "type": "double", "rw": True, "unit": "ml/h", "limites": (0, 50), "tag": "heparineTherapyDosage", "nivel": "cian"},   # 12
        0x06: {"name": "Cantidad de bolo", "label": "CANT. BOLO", "type": "double", "rw": True, "unit": "ml", "limites": (0, 10), "tag": "heparineBolusQuantity", "nivel": "cian"},                       # 13
        0x07: {"name": "Ajuste de velocidad de bomba bicarbonato", "label": "VEL BICARB", "type": "double", "rw": True, "unit": "%", "limites": (0, 100), "tag": "bicarbonatePumpSpeed", "nivel": "cian"},# 14
        0x08: {"name": "Ajuste de velocidad de ácido cítrico", "label": "VEL ACIDO", "type": "double", "rw": True, "unit": "%", "limites": (0, 100), "tag": "citricAcidPumpSpeed", "nivel": "cian"},     # 15
    },

    # ================================================================
    # CONTROL PID (0x04)
    # ================================================================
    0x04: {
        0x00: {"name": "Setpoint flujo sanguíneo", "label": "SP FLUJO S.", "type": "double", "rw": True, "unit": "ml/min", "limites": (0, 600), "tag": "bloodFlowControlSetPoint", "nivel": "cian"},        # 16
        0x01: {"name": "Cálculo flujo circuito sanguíneo", "label": "CALC FLUJO S.", "type": "double", "rw": True, "unit": "ml/min", "limites": (0, 600), "tag": "bloodFlowVariableData", "nivel": "cian"},   # 17 
        0x02: {"name": "Salida control flujo sanguíneo", "label": "OUT FLUJO S.", "type": "double", "rw": True, "unit": "%", "limites": (0, 100), "tag": "bloodFlowControlOutput", "nivel": "cian"},         # 18
        0x03: {"name": "Kp control de flujo sanguíneo", "label": "KP FLUJO S.", "type": "double", "rw": True, "unit": "", "limites": (0, 10), "tag": "bloodFlowControlPropGain", "nivel": "cian"},          # 19 
        0x04: {"name": "Ki control de flujo sanguíneo", "label": "KI FLUJO S.", "type": "double", "rw": True, "unit": "", "limites": (0, 10), "tag": "bloodFlowControlInteGain", "nivel": "cian"},          # 20
        0x05: {"name": "Kd control de flujo sanguíneo", "label": "KD FLUJO S.", "type": "double", "rw": True, "unit": "", "limites": (0, 10), "tag": "bloodFlowControlDeriGain", "nivel": "cian"},          # 21
        0x06: {"name": "Setpoint conductividad", "label": "SP COND.", "type": "double", "rw": True, "unit": "mS/cm", "limites": (13.0, 15.0), "tag": "dialyCondControlSetPoint", "nivel": "cian"},       # 22
        0x07: {"name": "Conductividad medida", "label": "COND. REAL", "type": "double", "rw": False, "unit": "mS/cm", "limites": (12.5, 15.5), "tag": "dialyCondVariableData", "nivel": "amarillo"},       # 23
        0x08: {"name": "Salida control de conductividad", "label": "OUT COND.", "type": "double", "rw": True, "unit": "%", "limites": (0, 100), "tag": "dialyCondControlOutput", "nivel": "cian"},       # 24
        0x09: {"name": "Kp control de conductividad", "label": "KP COND.", "type": "double", "rw": True, "unit": "", "limites": (0, 10), "tag": "dialyCondControlPropGain", "nivel": "cian"},            # 25
        0x0A: {"name": "Ki control de conductividad", "label": "KI COND.", "type": "double", "rw": True, "unit": "", "limites": (0, 10), "tag": "dialyCondControlInteGain", "nivel": "cian"},            # 26
        0x0B: {"name": "Kd control de conductividad", "label": "KD COND.", "type": "double", "rw": True, "unit": "", "limites": (0, 10), "tag": "dialyCondControlDeriGain", "nivel": "cian"},            # 27
        0x0C: {"name": "Setpoint temperatura", "label": "SP TEMP.", "type": "double", "rw": True, "unit": "°C", "limites": (35.0, 39.0), "tag": "dialyTempControlSetPoint", "nivel": "cian"},            # 28 
        0x0D: {"name": "Temperatura medida", "label": "TEMP. REAL", "type": "double", "rw": False, "unit": "°C", "limites": (34.5, 39.5), "tag": "dialyTempVariableData", "nivel": "amarillo"},            # 29
        0x0E: {"name": "Salida control temperatura", "label": "OUT TEMP.", "type": "double", "rw": True, "unit": "%", "limites": (0, 100), "tag": "dialyTempControlOutput", "nivel": "cian"},            # 30 
        0x0F: {"name": "Kp control temperatura", "label": "KP TEMP.", "type": "double", "rw": True, "unit": "", "limites": (0, 10), "tag": "dialyTempControlPropGain", "nivel": "cian"},                 # 31
        0x10: {"name": "Ki control temperatura", "label": "KI TEMP.", "type": "double", "rw": True, "unit": "", "limites": (0, 10), "tag": "dialyTempControlInteGain", "nivel": "cian"},                 # 32
        0x11: {"name": "Kd control temperatura", "label": "KD TEMP.", "type": "double", "rw": True, "unit": "", "limites": (0, 10), "tag": "dialyTempControlDeriGain", "nivel": "cian"},                 # 33
        0x12: {"name": "Ganancia Feedforward flujo", "label": "GAN FF FLUJO", "type": "double", "rw": True, "unit": "", "limites": (0, 5), "tag": "bloodFlowFeedForwardGain", "nivel": "cian"},              # 34
        0x13: {"name": "Tiempo adelanto Feedforward flujo", "label": "T. ADELANTO FF", "type": "double", "rw": True, "unit": "s", "limites": (0, 10), "tag": "bloodFlowFeedForwardLead", "nivel": "cian"},     # 35
        0x14: {"name": "Setpoint flujo dializante", "label": "SP FLUJO DIAL", "type": "double", "rw": True, "unit": "ml/min", "limites": (300, 800), "tag": "dialyFlowControlOutput", "nivel": "cian"},       # 36
        0x15: {"name": "Salida bomba de purga", "label": "OUT B.PURGA", "type": "double", "rw": True, "unit": "%", "limites": (0, 100), "tag": "dialyDeaerControlOutput", "nivel": "cian"},                # 37
        0x16: {"name": "Parámetro control variable 1", "label": "PARAM VAR 1", "type": "double", "rw": True, "unit": "", "limites": (0, 1000), "tag": "variableCtrlParamData1", "nivel": "cian"},           # 38
        0x17: {"name": "Parámetro control variable 2", "label": "PARAM VAR 2", "type": "double", "rw": True, "unit": "", "limites": (0, 1000), "tag": "variableCtrlParamData2", "nivel": "cian"},           # 39
        0x18: {"name": "Parámetro control variable 3", "label": "PARAM VAR 3", "type": "double", "rw": True, "unit": "", "limites": (0, 1000), "tag": "variableCtrlParamData3", "nivel": "cian"},           # 40
        0x19: {"name": "Parámetro control variable 4", "label": "PARAM VAR 4", "type": "double", "rw": True, "unit": "", "limites": (0, 1000), "tag": "variableCtrlParamData4", "nivel": "cian"},           # 41
        0x1A: {"name": "Parámetro control variable 5", "label": "PARAM VAR 5", "type": "double", "rw": True, "unit": "", "limites": (0, 1000), "tag": "variableCtrlParamData5", "nivel": "cian"},           # 42
    },

    # ================================================================
    # PROCESO - ANALÓGICAS (0x05)
    # ================================================================
    0x05: {
        0x00: {"name": "Velocidad bomba peristáltica de sangre", "label": "VEL B.SANGRE", "type": "double", "rw": True, "unit": "RPM", "limites": (0, 600), "tag": "bloodSpeedVariableData", "nivel": "cian"}, # 43
        0x01: {"name": "Flujo de heparina", "label": "FLUJO HEPAR", "type": "double", "rw": True, "unit": "ml/h", "limites": (0, 50), "tag": "heparFlowProcessData", "nivel": "cian"},                        # 44
        0x02: {"name": "Presión arterial en línea sanguínea", "label": "P. ARTERIAL", "type": "double", "rw": True, "unit": "mmHg", "limites": (-100, 400), "tag": "arterPresProcessData", "nivel": "rojo"},  # 45
        0x03: {"name": "Presión venosa en línea sanguínea", "label": "P. VENOSA", "type": "double", "rw": True, "unit": "mmHg", "limites": (-50, 300), "tag": "venouPresProcessData", "nivel": "rojo"},     # 46
        0x04: {"name": "Presión del dializante Entrada del filtro (EF)", "label": "P. DIAL ENT", "type": "double", "rw": True, "unit": "mmHg", "limites": (-200, 600), "tag": "dialyPresIFProcessData", "nivel": "amarillo"}, # 47
        0x05: {"name": "Presión del dializante Salida del filtro (SF)", "label": "P. DIAL SAL", "type": "double", "rw": True, "unit": "mmHg", "limites": (-200, 600), "tag": "dialyPresOFProcessData", "nivel": "amarillo"},  # 48
        0x06: {"name": "Presión entrada agua alimentación", "label": "P. AGUA RED", "type": "double", "rw": True, "unit": "bar", "limites": (0, 5), "tag": "dialyLineWaterPresData", "nivel": "cian"},        # 49
        0x07: {"name": "Temperatura del dializante EF", "label": "TEMP DIAL ENT", "type": "double", "rw": True, "unit": "°C", "limites": (35.0, 39.0), "tag": "dialyTempIFProcessData", "nivel": "amarillo"},   # 50
        0x08: {"name": "Temperatura del dializante SF", "label": "TEMP DIAL SAL", "type": "double", "rw": True, "unit": "°C", "limites": (35.0, 39.0), "tag": "dialyTempIOFProcessData", "nivel": "amarillo"},   # 51 
        0x09: {"name": "Flujo de líquido de sustitución", "label": "FLUJO SUST.", "type": "double", "rw": True, "unit": "ml/h", "limites": (0, 5000), "tag": "subsLiqFlowProcessData", "nivel": "cian"},      # 52
        0x0A: {"name": "Conductividad dializante antes del filtro", "label": "COND. PRE-F", "type": "double", "rw": True, "unit": "mS/cm", "limites": (13.0, 15.0), "tag": "dialyConductIFProcessData", "nivel": "amarillo"}, # 53
        0x0B: {"name": "Conductividad dializante después del filtro", "label": "COND. POST-F", "type": "double", "rw": True, "unit": "mS/cm", "limites": (13.0, 15.0), "tag": "dialyConductOFProcessData", "nivel": "amarillo"}, # 54
        0x0C: {"name": "Parametro de control ", "label": "FREC. CARD.", "type": "double", "rw": True, "unit": "lpm", "limites": (0,1000), "tag": "patHeartFreqProcessData", "nivel": "rojo"},     # 55 
        0x0D: {"name": "Presión en el tanque de calentamiento", "label": "P. TQ CALENT", "type": "double", "rw": True, "unit": "mmHg", "limites": (-100, 100), "tag": "dialyTankPresProcessData", "nivel": "cian"}, # 56
        0x0E: {"name": "Presión en la línea del dializante", "label": "P. LIN DIAL", "type": "double", "rw": True, "unit": "mmHg", "limites": (-200, 600), "tag": "dialyLinePresProcessData", "nivel": "amarillo"}, # 57
        0x0F: {"name": "Presión Prefiltrado", "label": "P. PRE-FILTRO", "type": "double", "rw": True, "unit": "mmHg", "limites": (0, 500), "tag": "dialyPFilPmpPresProcessData", "nivel": "cian"},              #58  
    },
    
    # ================================================================
    # CALIBRACIÓN - ANALÓGICAS (0x06) 
    # ================================================================
    0x06: {
        0x00: {"name": "Factor calibración bomba heparina", "label": "CAL HEPARINA", "type": "double", "rw": True, "unit": "ml/rev", "limites": (0.01, 10.0), "tag": "heparCalibFactorData", "nivel": "cian"},          # 59
        0x01: {"name": "Presión de ultrafiltrado", "label": "P. ULTRAFILT", "type": "double", "rw": True, "unit": "mmHg", "limites": (-50, 500), "tag": "dialyUFilPresProcessData", "nivel": "amarillo"},               # 60 
        0x02: {"name": "Presión en cámara de balance", "label": "P. CAM.BAL", "type": "double", "rw": False, "unit": "mmHg", "limites": (-100, 600), "tag": "dialyBChamPresProcessData", "nivel": "amarillo"},        # 61
        0x03: {"name": "Presión arterial del circuito de sangre", "label": "P. ART CIRC", "type": "double", "rw": False, "unit": "mmHg", "limites": (-300, 600), "tag": "bloodArteryPressureData", "nivel": "rojo"},   # 62 
        0x04: {"name": "Presión venosa del circuito de sangre", "label": "P. VEN CIRC", "type": "double", "rw": False, "unit": "mmHg", "limites": (-100, 500), "tag": "bloodVenousPressureData", "nivel": "rojo"},     # 63
        0x05: {"name": "Contador de ciclos de dialización", "label": "CONT CICLOS", "type": "double", "rw": False, "unit": "ciclos", "limites": (0, 100000), "tag": "dialyCycleOperationCount", "nivel": "cian"},      # 64
        0x06: {"name": "Factor calibración parámetro 7", "label": "CAL PARAM 7", "type": "double", "rw": True, "unit": "", "limites": (0.01, 100.0), "tag": "parameterCalFactData7", "nivel": "cian"},                 # 65
        0x07: {"name": "Parámetro control 8", "label": "PARAM CTRL 8", "type": "double", "rw": True, "unit": "", "limites": (0, 1000), "tag": "parameterControlData8", "nivel": "cian"},                                # 66
        0x08: {"name": "Parámetro control 9", "label": "PARAM CTRL 9", "type": "double", "rw": True, "unit": "", "limites": (0, 1000), "tag": "parameterControlData9", "nivel": "cian"},                                # 67
        0x09: {"name": "Parámetro control 10", "label": "PARAM CTRL 10", "type": "double", "rw": True, "unit": "", "limites": (0, 1000), "tag": "parameterControlData10", "nivel": "cian"},                              # 68
        0x0A: {"name": "Parámetro control 11", "label": "PARAM CTRL 11", "type": "double", "rw": True, "unit": "", "limites": (0, 1000), "tag": "parameterControlData11", "nivel": "cian"},                              # 69
        0x0B: {"name": "Parámetro control 12", "label": "PARAM CTRL 12", "type": "double", "rw": True, "unit": "", "limites": (0, 1000), "tag": "parameterControlData12", "nivel": "cian"},                              # 70
    },

    # ================================================================
    # BIOIMPEDANCIA Y UREA (0x07)
    # ================================================================
    0x07: {
        0x00: {"name": "BioZ Resistencia", "label": "BIOZ RESIST", "type": "double", "rw": False, "unit": "Ohm", "limites": (0, 1000), "tag": "bioz_resistance", "nivel": "cian"}, 
        0x01: {"name": "BioZ Fase", "label": "BIOZ FASE", "type": "double", "rw": False, "unit": "Deg", "limites": (-180, 180), "tag": "bioz_phase", "nivel": "cian"},           
        0x02: {"name": "Urea Sensor ADC1", "label": "UREA ADC 1", "type": "double", "rw": False, "unit": "ADC", "limites": (0, 4095), "tag": "urea_adc1", "nivel": "cian"},       
        0x03: {"name": "Urea Sensor ADC2", "label": "UREA ADC 2", "type": "double", "rw": False, "unit": "ADC", "limites": (0, 4095), "tag": "urea_adc2", "nivel": "cian"},       
    },

    0x08: {
        0x00: {"name": "patient_id","label": "ID PACIENTE","type": "string","rw": True,"unit": "","limites": None,"tag": "patient_id","nivel": "blanco"},
        0x01: {"name": "patient_name","label": "NOMBRE", "type": "string","rw": True,"unit": "","limites": None,"tag": "patient_name","nivel": "blanco"},
        0x02: {"name": "patient_gender","label": "GÉNERO","type": "int","rw": True,"unit": "","limites": None,"tag": "patient_gender","nivel": "blanco"},
        0x03: {"name": "patient_age","label": "EDAD","type": "int","rw": False, "unit": "años","limites": (0, 150),"tag": "patient_age","nivel": "blanco"},
        0x04: {"name": "patient_height_cm","label": "ESTATURA","type": "double","rw": False,"unit": "cm","limites": (50, 250),"tag": "patient_height_cm","nivel": "blanco"},
        0x05: {"name": "patient_dry_weight_kg","label": "PESO SECO","type": "double","rw": False,"unit": "kg","limites": (20, 200),"tag": "patient_dry_weight_kg","nivel": "blanco"},
        0x06: {"name": "patient_pre_weight_kg","label": "PESO PRE-DIAL","type": "double","rw": False,"unit": "kg","limites": (20, 200),"tag": "patient_pre_weight_kg","nivel": "blanco"},
        0x07: {"name": "uf_goal_liters","label": "OBJETIVO UF","type": "double","rw": True,"unit": "L","limites": (0.0, 10.0),"tag": "uf_goal_liters","nivel": "cian"},
    },
    0x09: {
        0x00: {"name": "pattern conductivity sensor", "label": "PATTERN_CONDUCTIVITY", "type": "double", "rw": True, "units": "mS/cm","limites": (0, 20), "tag": "patternCondSensor", "nivel":"cian"},
        0x01: {"name": "pattern temperature sensor", "label": "PATTERN_TEMPERATURE", "type": "double", "rw": True, "units": "°C","limites": (0, 100), "tag": "patternTempSensor", "nivel":"cian"},
        0x02: {"name": "pattern conductivity raw","label": "PATTERN_CONDUCTIVITY_RAW","type": "double","rw": True,"units": "mS/cm","limites": (0, 50), "tag": "patternCondRaw","nivel": "cian","value": 0.0,"description": "Conductividad sin compensación de temperatura (debug/calibración)" },
    },
    0x0A: {
        0x00: {"name": "Desinfection Mode", "label": "DESINFECTION_MODE", "type": "int", "rw": True, "units": "", "limites": None, "tag": "DesinftectionMode", "nivel": "cian"},
        0x01: {"name": "Desinfection mode 1 time hours", "label": "DT_HOURS", "type": "int", "rw":True, "units": None, "tag": "desinfection1TimeHours", "nivel": "cian"},
        0x02: {"name": "Desinfection mode 1 time minuts", "label": "DT_MIN", "type": "int", "rw": True, "units": None, "tag": "desinfection1TimeMin", "nivel": "cian"},
        0x03: {"name": "Desinfection mode 2 time hours", "label": "DT_HOURS", "type": "int", "rw":True, "units": None, "tag": "desinfection2TimeHours", "nivel": "cian"},
        0x04: {"name": "Desinfection mofr 2 time minuts", "label": "DT_MIN", "type": "int", "rw": True, "units": None, "tag": "desinfection2TimeMin", "nivel": "cian"},
    }
}

# ================================================================
# MAPEO DE LECTURA MASIVA ANALÓGICA (71 doubles)
# ================================================================
ANALOG_MAP: List[Tuple[int, int]] = [
    # 0x02 → 7 variables
    *( (0x02, i) for i in range(7) ),
    # 0x03 → 9 variables
    *( (0x03, i) for i in range(9) ),
    # 0x04 → 27 variables (0x00 a 0x1A)
    *( (0x04, i) for i in range(0x1B) ),
    # 0x05 → 16 variables específicas
    *( (0x05, i) for i in range(0x10) ),
    # 0x06 12 Variables de calibración)
    *( (0x06, i) for i in range(0x0C) )
]

# ================================================================
# GRUPOS PARA TABLAS
# ================================================================
TVAR_TO_GROUP = {
    0x01: "Operación",
    0x02: "Clínicos",
    0x03: "Setpoints",
    0x04: "Control PID",
    0x05: "Proceso",
    0x06: "Calibración",
    0x07: "Bioimpedancia y Urea",
    0x08: "Datos del paciente",
    0x09: "Sensor patron de conductividad",
    0x0A: "Modo de desinfección"
}



    
   

# Función CRC igual a la del HMI
crc16 = crcmod.mkCrcFun(0x18005, initCrc=0xFFFF, rev=True, xorOut=0x0000)

status_map = {
    1: "INICIO CEBADO", 2: "LLENADO DE TANQUE", 3: "LLENADO DE LINEA",
    4: "LLENADO CÁMARA", 5: "CALENTAMIENTO", 6: "INFUSIÓN",
    7: "COLOCACIÓN DE FILTRO", 8: "DIÁLISIS", 9: "BYPASS", 10: "CERRADO",
    12: "ULTRAFILTRACIÓN OFF", 13: "LISTO PARA INICIAR TRATAMIENTO",
    14: "TRATAMIENTO INICIADO", 15: "PAUSA", 16: "TRATAMIENTO DETENIDO"
}

treatment_mode_map = {
    0: "Hemodiálisis",
    1: "Hemodiafiltración",
    2: "Ultrafiltración",
    3: "Limpieza"
}

# Comandos de lectura fijos (del HMI)
READ_BOOLEAN_COMMAND = bytes.fromhex("11 11 00 3C")
READ_ANALOG_COMMAND = bytes.fromhex("12 AA 00 47")

# Tamaños de respuesta esperados (del HMI)
EXPECTED_BOOLEAN_RESPONSE_SIZE = 65  # 3 header + 60 data + 2 CRC
EXPECTED_ANALOG_RESPONSE_SIZE = 573  # 3 header + 71*8 bytes + 2 CRC
EXPECTED_WRITE_RESPONSE_SIZE = 6    # 3 header + 1 response byte + 2 CRC (comando 0x21/0x2x + 0x11/0xAA + ADDR + VAL/DATA + CRC)

# ================================================================
# WIDGET COMPONENTE LED
# ================================================================
class QLedIndicator(QWidget):
    """Representa un LED visual circular con estados de encendido y apagado."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(24, 24)
        self.status = False
        self.update_style()

    def set_state(self, state: bool):
        if self.status != state:
            self.status = state
            self.update_style()

    def update_style(self):
        if self.status:
            # Verde Brillante (Activo)
            style = """
                background-color: qradialgradient(cx:0.5, cy:0.5, radius:0.5, fx:0.4, fy:0.4, 
                                                  stop:0 #52D017, stop:1 #2C6B06);
                border: 2px solid #1E4603;
                border-radius: 12px;
            """
        else:
            # Gris / Verde Oscuro Opaco (Inactivo)
            style = """
                background-color: qradialgradient(cx:0.5, cy:0.5, radius:0.5, fx:0.4, fy:0.4, 
                                                  stop:0 #555555, stop:1 #222222);
                border: 2px solid #111111;
                border-radius: 12px;
            """
        self.setStyleSheet(style)
        


def _default_serial_port_name() -> str:
    """Puerto por defecto segun plataforma (Windows usa COMx, Linux/Ubuntu usa /dev/ttyUSB0)."""
    return "COM4" if sys.platform.startswith("win") else "/dev/ttyUSB0"

def get_simulation_mode() -> str:
    return os.getenv("SIMULATION_MODE", "real").strip().lower()

def get_simulation_port() -> str:
    configured_port = os.getenv("SIMULATION_SERIAL_PORT", "").strip()

    if configured_port:
        return configured_port

    if get_simulation_mode() == "simulation":
        if sys.platform.startswith("linux"):
            return os.path.expanduser(
                "~/.hemodialisis/simulador"
            )

        if sys.platform.startswith("win"):
            return "COM4"

    return _default_serial_port_name()

    


class Simulator(QWidget):
    request_led_update = Signal(int, bool)

    def __init__(self):
        super().__init__()
        self.serial_port = None
        self.running = False
        self.reader_thread = None
        # self.serial_port_name = os.environ.get("SIMULATOR_PORT", _default_serial_port_name())
        self.serial_port_name = get_simulation_port()

        self.realistic_mode = True

        self.current_simulated_values: Dict[int, Dict[int, Any]] = {}
        self.led_widgets = {}
        self.double_spin_widgets: Dict[Tuple[int, int], QDoubleSpinBox] = {}

        self._initialize_simulated_values()
        self.setup_ui()
        self.request_led_update.connect(self.update_led_visuals)
        self.start_serial(self.serial_port_name)

        


    def _get_var_info(self, group_code: int, var_id: int) -> Dict[str, Any]:
        return VARIABLES.get(group_code, {}).get(var_id, {})

    def _coerce_value(self, group_code: int, var_id: int, value: Any) -> Any:
        """Normaliza tipo y aplica límites definidos en el mapa de variables."""
        info = self._get_var_info(group_code, var_id)
        var_type = info.get("type")

        if var_type == "bool":
            coerced = bool(value)
        elif var_type == "int":
            coerced = int(round(float(value)))
        elif var_type == "double":
            coerced = float(value)
        elif var_type == "string":
            coerced = str(value)
        else:
            coerced = value

        limites = info.get("limites")
        if limites and isinstance(coerced, (int, float)):
            min_v, max_v = limites
            if min_v is not None:
                coerced = max(coerced, min_v)
            if max_v is not None:
                coerced = min(coerced, max_v)

            if var_type == "int":
                coerced = int(round(coerced))

        return coerced

    def _default_value_for_var(self, group_code: int, var_id: int, info: Dict[str, Any]) -> Any:
        if "value" in info:
            return info["value"]

        var_type = info.get("type")
        if var_type == "bool":
            return False
        if var_type == "string":
            return ""
        if var_type == "int":
            limites = info.get("limites")
            return int(limites[0]) if limites else 0

        name = info.get("name", "")
        tag = info.get("tag", "")
        if "Temp" in name or "TEMP" in tag:
            return 37.0
        if "Cond" in name or "COND" in tag:
            return 14.0
        return 0.0

    def _initialize_simulated_values(self):
        """Inicialización limpia"""
        for group_code, group_vars in VARIABLES.items():
            self.current_simulated_values[group_code] = {}
            for var_id, info in group_vars.items():
                default_value = self._default_value_for_var(group_code, var_id, info)
                self.current_simulated_values[group_code][var_id] = self._coerce_value(group_code, var_id, default_value)

        # Estados iniciales importantes
        self.current_simulated_values[0x02][2] = 1.0   # Estado cebado
        self.current_simulated_values[0x04][7] = 14.2
        self.current_simulated_values[0x05][7] = 36.8
        self.current_simulated_values[0x05][8] = 37.1

    def setup_ui(self):
        self.setWindowTitle("Simulador Hemodiálisis - Control Realista")
        self.resize(1200, 900)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        # Header
        title = QLabel("🔬 SIMULADOR DE CONTROLADOR HEMODIÁLISIS")
        title.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px; background: #2c3e50; color: white;")
        main_layout.addWidget(title)

        # Controles globales
        ctrl_layout = QHBoxLayout()
        self.chk_realistic = QCheckBox("Simulación Realista (con ruido)")
        self.chk_realistic.setChecked(True)
        self.chk_realistic.stateChanged.connect(self._toggle_realistic_mode)
        ctrl_layout.addWidget(self.chk_realistic)

        self.btn_randomize = QPushButton("🌡️ Randomizar Valores")
        self.btn_randomize.clicked.connect(self._randomize_values)
        ctrl_layout.addWidget(self.btn_randomize)
        main_layout.addLayout(ctrl_layout)
        # ================================================================
        # SECCIÓN SUPERIOR: ESTADO GENERAL DE OPERACIÓN
        # ================================================================
        top_layout = QHBoxLayout()

        # Estado del Proceso (0x02, 0x02)
        group_process = QGroupBox("Estado del Proceso Clínico")
        vbox_p = QVBoxLayout()
        self.combo_status = QComboBox()
        for key, value in status_map.items():
            self.combo_status.addItem(f"{key}: {value}", float(key))
        index = self.combo_status.findData(self.current_simulated_values[0x02][2])
        if index >= 0: self.combo_status.setCurrentIndex(index)
        self.combo_status.currentIndexChanged.connect(
            lambda idx: self._update_simulated_value(0x02, 2, self.combo_status.currentData())
        )
        vbox_p.addWidget(self.combo_status)
        group_process.setLayout(vbox_p)
        top_layout.addWidget(group_process)

        # Modo de Tratamiento (0x02, 0x01)
        group_mode = QGroupBox("Modo de Tratamiento Activo")
        vbox_m = QVBoxLayout()
        self.combo_treatment = QComboBox()
        for key, value in treatment_mode_map.items():
            self.combo_treatment.addItem(f"{key}: {value}", float(key))
        index = self.combo_treatment.findData(self.current_simulated_values[0x02][1])
        if index >= 0: self.combo_treatment.setCurrentIndex(index)
        self.combo_treatment.currentIndexChanged.connect(
            lambda idx: self._update_simulated_value(0x02, 1, self.combo_treatment.currentData())
        )
        vbox_m.addWidget(self.combo_treatment)
        group_mode.setLayout(vbox_m)
        top_layout.addWidget(group_mode)

        main_layout.addLayout(top_layout)

        # ================================================================
        # CONTENEDOR MULTI-PESTAÑA PARA VARIABLES EXPANDIDAS
        # ================================================================
        from PySide6.QtWidgets import QTabWidget, QScrollArea
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("QTabBar::tab { font-weight: bold; padding: 6px 12px; }")

        # ----------------------------------------------------------------
        # PESTAÑA 1: CIRCUITO SANGUÍNEO Y PACIENTE
        # ----------------------------------------------------------------
        tab_blood = QWidget()
        blood_grid = QGridLayout(tab_blood)

        # Bomba Peristáltica
        g_blood_pump = QGroupBox("Bomba Peristáltica de Sangre")
        v_bp = QVBoxLayout()
        self.spin_blood_flow = QSpinBox()
        self.spin_blood_flow.setRange(0, 600)
        self.spin_blood_flow.setSuffix(" RPM")
        self.spin_blood_flow.setValue(int(self.current_simulated_values[0x05][0]))
        self.spin_blood_flow.valueChanged.connect(lambda v: self._update_simulated_value(0x05, 0, float(v)))
        v_bp.addWidget(QLabel("Velocidad de Bomba (0x05, 0x00):"))
        v_bp.addWidget(self.spin_blood_flow)
        g_blood_pump.setLayout(v_bp)
        blood_grid.addWidget(g_blood_pump, 0, 0)

        # Presiones Hemodinámicas
        g_blood_pres = QGroupBox("Líneas de Presión Corporal")
        grid_bp = QGridLayout()
        
        self.spin_p_art = QSpinBox()
        self.spin_p_art.setRange(-100, 400)
        self.spin_p_art.setSuffix(" mmHg")
        self.spin_p_art.setValue(int(self.current_simulated_values[0x05][2]))
        self.spin_p_art.valueChanged.connect(lambda v: self._update_simulated_value(0x05, 2, float(v)))
        grid_bp.addWidget(QLabel("P. Arterial (0x05, 0x02):"), 0, 0)
        grid_bp.addWidget(self.spin_p_art, 0, 1)

        self.spin_p_ven = QSpinBox()
        self.spin_p_ven.setRange(-50, 300)
        self.spin_p_ven.setSuffix(" mmHg")
        self.spin_p_ven.setValue(int(self.current_simulated_values[0x05][3]))
        self.spin_p_ven.valueChanged.connect(lambda v: self._update_simulated_value(0x05, 3, float(v)))
        grid_bp.addWidget(QLabel("P. Venosa (0x05, 0x03):"), 1, 0)
        grid_bp.addWidget(self.spin_p_ven, 1, 1)
        g_blood_pres.setLayout(grid_bp)
        blood_grid.addWidget(g_blood_pres, 0, 1)

        # Datos Clínicos e Hidratación del Paciente (Grupo 0x08)
        g_patient = QGroupBox("Métricas del Paciente y Metas UF")
        grid_pat = QGridLayout()
        
        self.spin_pat_age = QSpinBox()
        self.spin_pat_age.setRange(0, 150)
        self.spin_pat_age.setValue(int(self.current_simulated_values[0x08][3]))
        self.spin_pat_age.valueChanged.connect(lambda v: self._update_simulated_value(0x08, 3, int(v)))
        grid_pat.addWidget(QLabel("Edad del Paciente (0x08, 0x03):"), 0, 0)
        grid_pat.addWidget(self.spin_pat_age, 0, 1)

        self.spin_uf_goal = QDoubleSpinBox()
        self.spin_uf_goal.setRange(0.0, 10.0)
        self.spin_uf_goal.setSingleStep(0.1)
        self.spin_uf_goal.setSuffix(" L")
        self.spin_uf_goal.setValue(float(self.current_simulated_values[0x08][7]))
        self.spin_uf_goal.valueChanged.connect(lambda v: self._update_simulated_value(0x08, 7, float(v)))
        grid_pat.addWidget(QLabel("Objetivo Total UF (0x08, 0x07):"), 1, 0)
        grid_pat.addWidget(self.spin_uf_goal, 1, 1)
        g_patient.setLayout(grid_pat)
        blood_grid.addWidget(g_patient, 1, 0, 1, 2)

        self.tabs.addTab(tab_blood, "🩸 Circuito Sanguíneo")

        # ----------------------------------------------------------------
        # PESTAÑA 2: CIRCUITO HIDRÁULICO (DIALIZANTE)
        # ----------------------------------------------------------------
        tab_dialy = QWidget()
        dialy_grid = QGridLayout(tab_dialy)

        # Conductividad Física e Hidráulica
        g_cond_group = QGroupBox("Módulo Químico (Conductividades)")
        grid_c = QGridLayout()
        
        self.spin_cond_real = QDoubleSpinBox()
        self.spin_cond_real.setRange(12.0, 16.0)
        self.spin_cond_real.setSingleStep(0.05)
        self.spin_cond_real.setSuffix(" mS/cm")
        self.spin_cond_real.setValue(self.current_simulated_values[0x04][7])
        self.spin_cond_real.valueChanged.connect(lambda v: self._update_simulated_value(0x04, 7, v))
        grid_c.addWidget(QLabel("Cond. Real Medida (0x04, 0x07):"), 0, 0)
        grid_c.addWidget(self.spin_cond_real, 0, 1)

        self.spin_cond_post = QDoubleSpinBox()
        self.spin_cond_post.setRange(13.0, 15.0)
        self.spin_cond_post.setSingleStep(0.05)
        self.spin_cond_post.setSuffix(" mS/cm")
        self.spin_cond_post.setValue(self.current_simulated_values[0x05][0x0B])
        self.spin_cond_post.valueChanged.connect(lambda v: self._update_simulated_value(0x05, 0x0B, v))
        grid_c.addWidget(QLabel("Cond. Post-Filtro (0x05, 0x0B):"), 1, 0)
        grid_c.addWidget(self.spin_cond_post, 1, 1)
        g_cond_group.setLayout(grid_c)
        dialy_grid.addWidget(g_cond_group, 0, 0)

        # Módulo Térmico
        g_temp_group = QGroupBox("Módulo Térmico")
        grid_t = QGridLayout()
        
        self.spin_temp_real = QDoubleSpinBox()
        self.spin_temp_real.setRange(34.0, 40.0)
        self.spin_temp_real.setSingleStep(0.1)
        self.spin_temp_real.setSuffix(" °C")
        self.spin_temp_real.setValue(self.current_simulated_values[0x05][7])
        self.spin_temp_real.valueChanged.connect(lambda v: self._update_simulated_value(0x05, 7, v))
        grid_t.addWidget(QLabel("Temp. Entrada Filtro EF (0x05, 0x07):"), 0, 0)
        grid_t.addWidget(self.spin_temp_real, 0, 1)

        self.spin_temp_out = QDoubleSpinBox()
        self.spin_temp_out.setRange(34.0, 40.0)
        self.spin_temp_out.setSingleStep(0.1)
        self.spin_temp_out.setSuffix(" °C")
        self.spin_temp_out.setValue(self.current_simulated_values[0x05][8])
        self.spin_temp_out.valueChanged.connect(lambda v: self._update_simulated_value(0x05, 8, v))
        grid_t.addWidget(QLabel("Temp. Salida Filtro SF (0x05, 0x08):"), 1, 0)
        grid_t.addWidget(self.spin_temp_out, 1, 1)
        g_temp_group.setLayout(grid_t)
        dialy_grid.addWidget(g_temp_group, 0, 1)

        # Presiones del Dializante e Hidráulica interna
        g_hydra_pres = QGroupBox("Presión de Cámara de Balance y Filtros")
        grid_hp = QGridLayout()
        
        self.spin_p_dial_in = QSpinBox()
        self.spin_p_dial_in.setRange(-200, 600)
        self.spin_p_dial_in.setSuffix(" mmHg")
        self.spin_p_dial_in.setValue(int(self.current_simulated_values[0x05][4]))
        self.spin_p_dial_in.valueChanged.connect(lambda v: self._update_simulated_value(0x05, 4, float(v)))
        grid_hp.addWidget(QLabel("Presión Dializante Ent. Filtro EF (0x05, 0x04):"), 0, 0)
        grid_hp.addWidget(self.spin_p_dial_in, 0, 1)

        self.spin_p_dial_out = QSpinBox()
        self.spin_p_dial_out.setRange(-200, 600)
        self.spin_p_dial_out.setSuffix(" mmHg")
        self.spin_p_dial_out.setValue(int(self.current_simulated_values[0x05][5]))
        self.spin_p_dial_out.valueChanged.connect(lambda v: self._update_simulated_value(0x05, 5, float(v)))
        grid_hp.addWidget(QLabel("Presión Dializante Sal. Filtro SF (0x05, 0x05):"), 1, 0)
        grid_hp.addWidget(self.spin_p_dial_out, 1, 1)

        self.spin_p_bal_chamb = QSpinBox()
        self.spin_p_bal_chamb.setRange(-100, 600)
        self.spin_p_bal_chamb.setSuffix(" mmHg")
        self.spin_p_bal_chamb.setValue(int(self.current_simulated_values[0x06][2]))
        self.spin_p_bal_chamb.valueChanged.connect(lambda v: self._update_simulated_value(0x06, 2, float(v)))
        grid_hp.addWidget(QLabel("Presión Cámara Balance Real (0x06, 0x02):"), 2, 0)
        grid_hp.addWidget(self.spin_p_bal_chamb, 2, 1)
        g_hydra_pres.setLayout(grid_hp)
        dialy_grid.addWidget(g_hydra_pres, 1, 0, 1, 2)

        # Tiempos de Configuración Hidráulica (Ciclos de Balance)
        g_cycles = QGroupBox("Configuración Ciclos de Volumen e Infusión")
        grid_cy = QGridLayout()
        
        self.spin_time_bal = QDoubleSpinBox()
        self.spin_time_bal.setRange(0, 100)
        self.spin_time_bal.setSuffix(" s")
        self.spin_time_bal.setValue(float(self.current_simulated_values[0x03][1]))
        self.spin_time_bal.valueChanged.connect(lambda v: self._update_simulated_value(0x03, 1, v))
        grid_cy.addWidget(QLabel("Tiempo Ciclo Cámara Balance (0x03, 0x01):"), 0, 0)
        grid_cy.addWidget(self.spin_time_bal, 0, 1)

        self.spin_uf_rate = QDoubleSpinBox()
        self.spin_uf_rate.setRange(0.0, 2.0)
        self.spin_uf_rate.setSingleStep(0.05)
        self.spin_uf_rate.setSuffix(" L/h")
        self.spin_uf_rate.setValue(float(self.current_simulated_values[0x03][0]))
        self.spin_uf_rate.valueChanged.connect(lambda v: self._update_simulated_value(0x03, 0, v))
        grid_cy.addWidget(QLabel("Tasa Velocidad Ultrafiltración (0x03, 0x00):"), 1, 0)
        grid_cy.addWidget(self.spin_uf_rate, 1, 1)
        g_cycles.setLayout(grid_cy)
        dialy_grid.addWidget(g_cycles, 2, 0, 1, 2)

        self.tabs.addTab(tab_dialy, "💧 Circuito Hidráulico (Dializante)")

        # ----------------------------------------------------------------
        # PESTAÑA 3: LAZOS PID Y SINTONIZACIÓN INDUSTRIAL
        # ----------------------------------------------------------------
        tab_pid = QWidget()
        pid_grid = QGridLayout(tab_pid)

        # PID Flujo sanguineo (incluye bloodFlowVariableData)
        g_pid_flow = QGroupBox("Lazo de Sintonización - Flujo Sanguíneo")
        grid_pf = QGridLayout()

        self.spin_sp_blood = QDoubleSpinBox()
        self.spin_sp_blood.setRange(0, 600)
        self.spin_sp_blood.setSuffix(" ml/min")
        self.spin_sp_blood.setValue(float(self.current_simulated_values[0x04][0x00]))
        self.spin_sp_blood.valueChanged.connect(lambda v: self._update_simulated_value(0x04, 0x00, v))
        grid_pf.addWidget(QLabel("Setpoint Flujo (tag: bloodFlowControlSetPoint, 0x04, 0x00):"), 0, 0)
        grid_pf.addWidget(self.spin_sp_blood, 0, 1)

        self.spin_blood_flow_variable = QDoubleSpinBox()
        self.spin_blood_flow_variable.setRange(0, 600)
        self.spin_blood_flow_variable.setSuffix(" ml/min")
        self.spin_blood_flow_variable.setValue(float(self.current_simulated_values[0x04][0x01]))
        self.spin_blood_flow_variable.valueChanged.connect(lambda v: self._update_simulated_value(0x04, 0x01, v))
        grid_pf.addWidget(QLabel("Flujo Calculado (tag: bloodFlowVariableData, 0x04, 0x01):"), 1, 0)
        grid_pf.addWidget(self.spin_blood_flow_variable, 1, 1)

        g_pid_flow.setLayout(grid_pf)
        pid_grid.addWidget(g_pid_flow, 0, 0, 1, 2)

        # PID Conductividad
        g_pid_cond = QGroupBox("Lazo de Sintonización - Conductividad")
        grid_pc = QGridLayout()
        self.spin_kp_cond = QDoubleSpinBox(); self.spin_kp_cond.setRange(0, 10); self.spin_kp_cond.setValue(self.current_simulated_values[0x04][9])
        self.spin_kp_cond.valueChanged.connect(lambda v: self._update_simulated_value(0x04, 0x09, v))
        grid_pc.addWidget(QLabel("Proporcional Kp (0x04, 0x09):"), 0, 0)
        grid_pc.addWidget(self.spin_kp_cond, 0, 1)
        
        self.spin_ki_cond = QDoubleSpinBox(); self.spin_ki_cond.setRange(0, 10); self.spin_ki_cond.setValue(self.current_simulated_values[0x04][0x0A])
        self.spin_ki_cond.valueChanged.connect(lambda v: self._update_simulated_value(0x04, 0x0A, v))
        grid_pc.addWidget(QLabel("Integral Ki (0x04, 0x0A):"), 1, 0)
        grid_pc.addWidget(self.spin_ki_cond, 1, 1)
        g_pid_cond.setLayout(grid_pc)
        pid_grid.addWidget(g_pid_cond, 1, 0)

        # PID Temperatura
        g_pid_temp = QGroupBox("Lazo de Sintonización - Temperatura")
        grid_pt = QGridLayout()
        self.spin_kp_temp = QDoubleSpinBox(); self.spin_kp_temp.setRange(0, 10); self.spin_kp_temp.setValue(self.current_simulated_values[0x04][0x0F])
        self.spin_kp_temp.valueChanged.connect(lambda v: self._update_simulated_value(0x04, 0x0F, v))
        grid_pt.addWidget(QLabel("Proporcional Kp (0x04, 0x0F):"), 0, 0)
        grid_pt.addWidget(self.spin_kp_temp, 0, 1)
        
        self.spin_ki_temp = QDoubleSpinBox(); self.spin_ki_temp.setRange(0, 10); self.spin_ki_temp.setValue(self.current_simulated_values[0x04][0x10])
        self.spin_ki_temp.valueChanged.connect(lambda v: self._update_simulated_value(0x04, 0x10, v))
        grid_pt.addWidget(QLabel("Integral Ki (0x04, 0x10):"), 1, 0)
        grid_pt.addWidget(self.spin_ki_temp, 1, 1)
        g_pid_temp.setLayout(grid_pt)
        pid_grid.addWidget(g_pid_temp, 1, 1)

        self.tabs.addTab(tab_pid, "🎛️ Lazos PID Control")

        # ----------------------------------------------------------------
        # PESTAÑA 4: MANTENIMIENTO, DESINFECCIÓN Y PATRONES
        # ----------------------------------------------------------------
        tab_maint = QWidget()
        maint_grid = QGridLayout(tab_maint)

        # Modos Sanidad/Desinfección (0x0A)
        g_desinf = QGroupBox("Parámetros del Ciclo de Sanitización")
        grid_d = QGridLayout()
        
        self.spin_des_mode = QSpinBox()
        self.spin_des_mode.setRange(0, 5)
        self.spin_des_mode.setValue(int(self.current_simulated_values[0x0A][0]))
        self.spin_des_mode.valueChanged.connect(lambda v: self._update_simulated_value(0x0A, 0, int(v)))
        grid_d.addWidget(QLabel("Modo de Desinfección Activo (0x0A, 0x00):"), 0, 0)
        grid_d.addWidget(self.spin_des_mode, 0, 1)

        self.spin_des_h = QSpinBox()
        self.spin_des_h.setRange(0, 24)
        self.spin_des_h.setSuffix(" Horas")
        self.spin_des_h.setValue(int(self.current_simulated_values[0x0A][1]))
        self.spin_des_h.valueChanged.connect(lambda v: self._update_simulated_value(0x0A, 1, int(v)))
        grid_d.addWidget(QLabel("Tiempo Programado M1 (0x0A, 0x01):"), 1, 0)
        grid_d.addWidget(self.spin_des_h, 1, 1)
        g_desinf.setLayout(grid_d)
        maint_grid.addWidget(g_desinf, 0, 0)

        # Sensores Patrón de Verificación (0x09)
        g_pattern = QGroupBox("Sensores Patrón Externos (Calibración HMI)")
        grid_patt = QGridLayout()
        
        self.spin_patt_cond = QDoubleSpinBox()
        self.spin_patt_cond.setRange(0.0, 20.0)
        self.spin_patt_cond.setSuffix(" mS/cm")
        self.spin_patt_cond.setValue(self.current_simulated_values[0x09][0])
        self.spin_patt_cond.valueChanged.connect(lambda v: self._update_simulated_value(0x09, 0, v))
        grid_patt.addWidget(QLabel("Sensor Patrón Conductividad (0x09, 0x00):"), 0, 0)
        grid_patt.addWidget(self.spin_patt_cond, 0, 1)

        self.spin_patt_temp = QDoubleSpinBox()
        self.spin_patt_temp.setRange(0.0, 100.0)
        self.spin_patt_temp.setSuffix(" °C")
        self.spin_patt_temp.setValue(self.current_simulated_values[0x09][1])
        self.spin_patt_temp.valueChanged.connect(lambda v: self._update_simulated_value(0x09, 1, v))
        grid_patt.addWidget(QLabel("Sensor Patrón Temperatura (0x09, 0x01):"), 1, 0)
        grid_patt.addWidget(self.spin_patt_temp, 1, 1)
        g_pattern.setLayout(grid_patt)
        maint_grid.addWidget(g_pattern, 0, 1)

        self.tabs.addTab(tab_maint, "🛠️ Desinfección y Calibración")

        # ----------------------------------------------------------------
        # NUEVA PESTAÑA 5: MATRIZ DE LEDS (VARIABLES DIGITALES 0x01)
        # ----------------------------------------------------------------
        tab_leds = QWidget()
        layout_leds = QVBoxLayout(tab_leds)
        layout_leds.setContentsMargins(5, 5, 5, 5)

        grp_leds = QGroupBox("ESTADO DE VARIABLES DIGITALES (0x01) - LEDS EN TIEM realtime")
        grp_leds.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; color: #2c3e50; }")
        grid_leds_layout = QGridLayout(grp_leds)
        grid_leds_layout.setSpacing(6)

        # Construcción dinámica de la grilla de LEDs (4 columnas)
        max_columns = 4
        bool_vars = VARIABLES[0x01]
        
                
        for var_id, var_info in bool_vars.items():
            row = var_id // max_columns
            col = var_id % max_columns

            cell_widget = QWidget()
            cell_layout = QHBoxLayout(cell_widget)
            cell_layout.setContentsMargins(5, 2, 5, 2)
            
            led = QLedIndicator()
            self.led_widgets[var_id] = led 
            
            # Convertimos el Label en un PushButton transparente para que sea interactivo
            btn_trigger = QPushButton(f"[{var_id:02d}] {var_info['label']}")
            btn_trigger.setStyleSheet("""
                QPushButton { 
                    text-align: left;
                    border: 1px solid #cbd5e1;
                    border-radius: 4px;
                    background: #f8fafc;
                    font-size: 11px;
                    color: #0b3a66;
                    font-weight: 600;
                    padding: 4px 6px;
                }
                QPushButton:hover { background-color: #e2e8f0; border-color: #94a3b8; }
                QPushButton:pressed { background-color: #cbd5e1; }
            """)
            
            # Conexión: Al hacer clic en el nombre, se invierte el valor
            btn_trigger.clicked.connect(lambda checked=False, vid=var_id: self._manual_toggle_bool(vid))
            
            cell_layout.addWidget(led)
            cell_layout.addWidget(btn_trigger)
            cell_layout.addStretch()

            grid_leds_layout.addWidget(cell_widget, row, col)


        # ScrollArea para contener la matriz de LEDs de forma responsiva
        scroll_leds = QScrollArea()
        scroll_leds.setWidgetResizable(True)
        scroll_leds.setWidget(grp_leds)
        layout_leds.addWidget(scroll_leds)

        self.tabs.addTab(tab_leds, "🟢 Matriz de LEDs (0x01)")

        # ----------------------------------------------------------------
        # NUEVA PESTAÑA 6: MATRIZ DE TAGS DOUBLE
        # ----------------------------------------------------------------
        tab_doubles = QWidget()
        layout_doubles = QVBoxLayout(tab_doubles)
        layout_doubles.setContentsMargins(5, 5, 5, 5)

        grp_doubles = QGroupBox("TAGS DOUBLE (lectura/escritura por simulador)")
        grp_doubles.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; color: #1e3a8a; }")
        grid_doubles = QGridLayout(grp_doubles)
        grid_doubles.setSpacing(8)

        row = 0
        for group_code, group_vars in VARIABLES.items():
            for var_id, var_info in group_vars.items():
                if var_info.get("type") != "double":
                    continue

                tag = var_info.get("tag", f"g{group_code:02X}_{var_id:02d}")
                group_text = f"G:0x{group_code:02X} ID:{var_id:02d}"
                unit = var_info.get("unit") or var_info.get("units") or ""
                rw = var_info.get("rw", True)

                lbl_tag = QLabel(f"{tag}")
                lbl_tag.setStyleSheet("color: #ffffff; font-weight: 700;")
                grid_doubles.addWidget(lbl_tag, row, 0)

                lbl_meta = QLabel(f"{group_text} {'RW' if rw else 'RO'}")
                lbl_meta.setStyleSheet("color:#ffffff; font-size: 11px;")
                grid_doubles.addWidget(lbl_meta, row, 1)

                spin = QDoubleSpinBox()
                limits = var_info.get("limites")
                if limits and isinstance(limits, tuple) and len(limits) == 2:
                    spin.setRange(float(limits[0]), float(limits[1]))
                else:
                    spin.setRange(-1_000_000.0, 1_000_000.0)

                spin.setDecimals(4)
                spin.setSingleStep(0.1)
                if unit:
                    spin.setSuffix(f" {unit}")

                value = float(self.current_simulated_values.get(group_code, {}).get(var_id, 0.0))
                spin.setValue(value)

                if rw:
                    spin.valueChanged.connect(lambda v, gc=group_code, vid=var_id: self._update_simulated_value(gc, vid, v))
                else:
                    spin.setReadOnly(True)
                    spin.setButtonSymbols(QDoubleSpinBox.NoButtons)
                    spin.setStyleSheet("background-color: #f1f5f9; color: #334155;")

                self.double_spin_widgets[(group_code, var_id)] = spin
                grid_doubles.addWidget(spin, row, 2)
                row += 1

        scroll_doubles = QScrollArea()
        scroll_doubles.setWidgetResizable(True)
        scroll_doubles.setWidget(grp_doubles)
        layout_doubles.addWidget(scroll_doubles)

        self.tabs.addTab(tab_doubles, "🔵 Tags Double")

        # ----------------------------------------------------------------
        # NUEVA PESTAÑA 7: PUERTO SERIAL
        # ----------------------------------------------------------------
        tab_serial = QWidget()
        layout_serial = QVBoxLayout(tab_serial)
        layout_serial.setContentsMargins(10, 10, 10, 10)

        grp_serial = QGroupBox("Conexión Serial")
        grp_serial.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        serial_form = QVBoxLayout(grp_serial)

        row_serial = QHBoxLayout()
        self.chk_serial_enable = QCheckBox("Habilitar puerto")
        self.chk_serial_enable.setChecked(True)
        row_serial.addWidget(self.chk_serial_enable)

        row_serial.addWidget(QLabel("Puerto:"))
        self.combo_serial_port = QComboBox()
        self.combo_serial_port.setMinimumWidth(160)
        row_serial.addWidget(self.combo_serial_port)

        self.btn_refresh_serial = QPushButton("Actualizar puertos")
        self.btn_refresh_serial.clicked.connect(self._refresh_serial_ports)
        row_serial.addWidget(self.btn_refresh_serial)

        self.btn_apply_serial = QPushButton("Aplicar")
        self.btn_apply_serial.clicked.connect(self._apply_serial_settings)
        row_serial.addWidget(self.btn_apply_serial)

        row_serial.addStretch()
        serial_form.addLayout(row_serial)

        self.lbl_serial_status = QLabel("Estado: Desconectado")
        self.lbl_serial_status.setStyleSheet("color: #7f8c8d; font-weight: bold; padding: 5px;")
        serial_form.addWidget(self.lbl_serial_status)

        layout_serial.addWidget(grp_serial)
        layout_serial.addStretch()

        self._populate_serial_combo(preferred=self.serial_port_name)

        self.tabs.addTab(tab_serial, "🔌 Puerto Serial")

        # Adjuntar pestañas completas al diseño general
        main_layout.addWidget(self.tabs)

        # ================================================================
        # SECCIÓN INFERIOR: ALARMAS RÁPIDAS INDUSTRIALES Y ESTADOS SERIALES
        # ================================================================
        alarm_group = QGroupBox("Disparadores de Alarma de Planta Críticos (Booleanos 0x01)")
        alarm_hbox = QHBoxLayout()
        self.btn_air = QPushButton("🚨 Aire en Línea")
        self.btn_blood = QPushButton("🚨 Fuga de Sangre")
        self.btn_air.clicked.connect(self._toggle_air_bubble)
        self.btn_blood.clicked.connect(self._toggle_blood_leak)
        alarm_hbox.addWidget(self.btn_air)
        alarm_hbox.addWidget(self.btn_blood)
        alarm_group.setLayout(alarm_hbox)
        main_layout.addWidget(alarm_group)

        # Estado Final del Enlace Serial
        self.info_label = QLabel("Simulador activo - Enlace desconectado")
        self.info_label.setStyleSheet("color: #7f8c8d; font-weight: bold; padding: 5px;")
        main_layout.addWidget(self.info_label)

        main_layout.addStretch()

    def _toggle_realistic_mode(self, state):
        self.realistic_mode = bool(state)

    def _randomize_values(self):
        """Útil para pruebas rápidas."""
        for group_code, group_values in self.current_simulated_values.items():
            for var_id, current_value in group_values.items():
                info = self._get_var_info(group_code, var_id)
                if not info.get("rw", True):
                    continue

                var_type = info.get("type")
                if var_type == "double":
                    delta = random.uniform(-2.0, 2.0)
                    self._update_simulated_value(group_code, var_id, float(current_value) + delta)
                elif var_type == "int":
                    delta = random.randint(-2, 2)
                    self._update_simulated_value(group_code, var_id, int(current_value) + delta)
                elif var_type == "bool" and random.random() < 0.1:
                    self._update_simulated_value(group_code, var_id, not bool(current_value))
                    
    def _update_simulated_value(self, group_code, var_id, value):
        """Actualiza un valor en el estado interno del simulador."""
        if group_code in self.current_simulated_values and var_id in self.current_simulated_values[group_code]:
            normalized = self._coerce_value(group_code, var_id, value)
            self.current_simulated_values[group_code][var_id] = normalized
            print(f"[SIMULATOR] Valor interno actualizado: G:{hex(group_code)} ID:{var_id} = {normalized}")
        else:
            print(f"[SIMULATOR] Advertencia: Intentando actualizar valor no mapeado: G:{hex(group_code)} ID:{var_id} = {value}")

    def _toggle_blood_leak(self):
        current_state = self.current_simulated_values[0x01][49]
        new_state = not current_state
        self._update_simulated_value(0x01, 49, new_state)
        # Notificar a la matriz de LEDs
        self.request_led_update.emit(49, new_state)
        
        if new_state:
            self.btn_blood.setText("🚨 FUGA DE SANGRE: ACTIVA")
            self.btn_blood.setStyleSheet("background-color: #dc2626; color: white; font-weight: bold; height: 50px;")
        else:
            self.btn_blood.setText("🚨 Fuga de Sangre: OFF")
            self.btn_blood.setStyleSheet("background-color: #d1d5db; color: black; height: 50px;")

    def _toggle_air_bubble(self):
        current_state = self.current_simulated_values[0x01][48]
        new_state = not current_state
        self._update_simulated_value(0x01, 48, new_state)
        # Notificar a la matriz de LEDs
        self.request_led_update.emit(48, new_state)
        
        if new_state:
            self.btn_air.setText("🚨 AIRE EN LÍNEA: ACTIVA")
            self.btn_air.setStyleSheet("background-color: #dc2626; color: white; font-weight: bold; height: 50px;")
        else:
            self.btn_air.setText("🚨 Aire en Línea: OFF")
            self.btn_air.setStyleSheet("background-color: #d1d5db; color: black; height: 50px;")

    def _manual_toggle_bool(self, var_id):
        """Permite cambiar booleanos haciendo clic en la matriz de LEDs."""
        current = self.current_simulated_values[0x01].get(var_id, False)
        new_val = not current
        self._update_simulated_value(0x01, var_id, new_val)
        self.request_led_update.emit(var_id, new_val)
        
        # Si son las alarmas críticas, actualizar también los botones de la pestaña principal
        if var_id == 48: # Aire
            self._update_alarm_button_style(self.btn_air, "Aire en Línea", new_val)
        elif var_id == 49: # Sangre
            self._update_alarm_button_style(self.btn_blood, "Fuga de Sangre", new_val)

    def _update_alarm_button_style(self, button, text, is_active):
        """Helper para mantener los botones de alarma sincronizados."""
        if is_active:
            button.setText(f"🚨 {text.upper()}: ACTIVA")
            button.setStyleSheet("background-color: #dc2626; color: white; font-weight: bold; height: 50px;")
        else:
            button.setText(f"🚨 {text}: OFF")
            button.setStyleSheet("background-color: #d1d5db; color: black; height: 50px;")



# ====================== SERIAL ======================
    def start_serial(self, port_name):
        try:
            self.serial_port = serial.Serial(port_name, 115200, timeout=0.05)
            self.running = True
            self.reader_thread = threading.Thread(target=self.serial_loop, daemon=True)
            self.reader_thread.start()
            print(f"✅ Simulador escuchando en {port_name}")
            if hasattr(self, "console_display"):
                self.log_message(f"Puerto serial conectado en {port_name}.")
            self._update_serial_status(True, port_name)
        except Exception as e:
            self.serial_port = None
            self.running = False
            print(f"❌ Error abriendo puerto {port_name}: {e}")
            if hasattr(self, "console_display"):
                self.log_message(f"Sin puerto serial disponible ({port_name}); modo simulación local activo.")
            self._update_serial_status(False, port_name, error=str(e))

    def stop_serial(self):
        self.running = False
        if self.reader_thread and self.reader_thread.is_alive():
            self.reader_thread.join(timeout=1.0)
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        self.serial_port = None
        self.reader_thread = None

    def _list_serial_ports(self):
        try:
            ports = [
                port.device
                for port in serial.tools.list_ports.comports()
            ]
            if (
                sys.platform.startswith("linux")
                and get_simulation_mode() == "simulation"
            ):
                virtual_port = os.path.expanduser(
                    "~/.hemodialisis/simulador"
                )

                if (
                    os.path.exists(virtual_port)
                    and virtual_port not in ports
                ):
                    ports.append(virtual_port)

            configured_port = os.getenv("SIMULATOR_SERIAL_PORT","").strip()

            if (
                configured_port
                and os.path.exists(configured_port)
                and configured_port not in ports
            ):
                ports.append(configured_port)

            return ports

        except Exception as error:
            print(f"[SIMULATOR] Error listando puertos: {error}")
            return []



        

    def _populate_serial_combo(self, preferred=None, strict=False):
        """strict=True no aplica fallback al puerto por defecto/primer puerto (usado al refrescar)."""
        ports = self._list_serial_ports()
        self.combo_serial_port.blockSignals(True)
        self.combo_serial_port.clear()
        self.combo_serial_port.addItems(ports)

        default_port = _default_serial_port_name()
        selected = None
        if preferred and preferred in ports:
            selected = preferred
        elif not strict:
            if default_port in ports:
                selected = default_port
            elif ports:
                selected = ports[0]

        if selected:
            self.combo_serial_port.setCurrentText(selected)

        self.combo_serial_port.blockSignals(False)

    def _refresh_serial_ports(self):
        current = self.combo_serial_port.currentText()
        self._populate_serial_combo(preferred=current, strict=True)

    def _apply_serial_settings(self):
        if not self.chk_serial_enable.isChecked():
            self.stop_serial()
            self._update_serial_status(False, self.combo_serial_port.currentText())
            return

        port_name = self.combo_serial_port.currentText().strip()
        if not port_name:
            self._update_serial_status(False, "", error="Ningún puerto seleccionado")
            return

        if port_name not in self._list_serial_ports():
            self._update_serial_status(False, port_name, error="El puerto ya no está disponible")
            return

        self.stop_serial()
        self.serial_port_name = port_name
        self.start_serial(port_name)

    def _update_serial_status(self, connected, port_name, error=None):
        if connected:
            text = f"Estado: Conectado ({port_name})"
            style = "color: #16a34a; font-weight: bold; padding: 5px;"
            info_text = f"Simulador activo - Enlace conectado en {port_name}"
        elif error:
            text = f"Estado: Error ({port_name}): {error}"
            style = "color: #dc2626; font-weight: bold; padding: 5px;"
            info_text = f"Simulador activo - Enlace desconectado ({error})"
        else:
            text = "Estado: Desconectado"
            style = "color: #7f8c8d; font-weight: bold; padding: 5px;"
            info_text = "Simulador activo - Enlace desconectado"

        if hasattr(self, "lbl_serial_status"):
            self.lbl_serial_status.setText(text)
            self.lbl_serial_status.setStyleSheet(style)
        if hasattr(self, "info_label"):
            self.info_label.setText(info_text)

    def serial_loop(self):
        buffer = bytearray()
        while self.running and self.serial_port and self.serial_port.is_open:
            try:
                if self.serial_port.in_waiting:
                    buffer.extend(self.serial_port.read(self.serial_port.in_waiting))

                while len(buffer) >= 6:
                    # Lectura booleana: 0x11 0x11 0x00 + CRC(2)
                    if buffer[:3] == b'\x11\x11\x00':
                        frame = bytes(buffer[:6])
                        if self._validate_frame_crc(frame):
                            self._handle_boolean_read()
                        del buffer[:6]
                    # Lectura analógica: 0x12 0xAA 0x00 + CRC(2)
                    elif buffer[:3] == b'\x12\xAA\x00':
                        frame = bytes(buffer[:6])
                        if self._validate_frame_crc(frame):
                            self._handle_analog_read()
                        del buffer[:6]
                    # Escritura booleana: 0x21 0x11 ADDR VAL + CRC(2)
                    elif buffer[:2] == b'\x21\x11':
                        frame = bytes(buffer[:6])
                        if self._validate_frame_crc(frame):
                            self._handle_boolean_write(frame[:4])
                        del buffer[:6]
                    # Escritura double: 0x2G 0xAA ADDR + 8 bytes + CRC(2)
                    elif (buffer[0] & 0xF0) == 0x20 and buffer[1] == 0xAA:
                        if len(buffer) < 13:
                            break
                        frame = bytes(buffer[:13])
                        if self._validate_frame_crc(frame):
                            self._handle_double_write(frame[:11])
                        del buffer[:13]
                    else:
                        # Re-sincronización ante ruido o bytes fuera de protocolo
                        del buffer[0]


                time.sleep(0.001)
            except Exception as e:
                print(f"[SIMULATOR ERROR] {e}")
                time.sleep(0.1)

    def _validate_frame_crc(self, frame: bytes) -> bool:
        """Valida CRC de una trama completa (payload + 2 bytes CRC)."""
        if len(frame) < 3:
            return False

        payload = frame[:-2]
        rx_crc = (frame[-2] << 8) | frame[-1]
        calc_crc = crc16(payload)
        if rx_crc != calc_crc:
            print(f"[SIMULATOR] CRC inválido. RX=0x{rx_crc:04X} CALC=0x{calc_crc:04X}")
            return False
        return True

   
# ====================== NUEVA LÓGICA AUTOMÁTICA ESTADO 7 ======================
    def _auto_handle_filter_fill(self, status_code: int):
        """Cuando llega al estado 7, activa automáticamente el botón de llenado de filtro"""
        if status_code == 7:
            if 0x01 in self.current_simulated_values:
                if 56 not in self.current_simulated_values[0x01] or not self.current_simulated_values[0x01][56]:
                    self.current_simulated_values[0x01][56] = True  # "dialyFilterFillButton"
                    self.request_led_update.emit(56, True)
                    print("🔧 [AUTO] Estado 7 detectado → Activando 'dialyFilterFillButton' automáticamente")
                    
                    # Opcional: simular que el usuario ya colocó el filtro después de 8 segundos
                    QTimer.singleShot(8000, lambda: self._auto_complete_filter_placement())

    def _auto_complete_filter_placement(self):
        """Simula que el filtro ya fue colocado y avanza el estado"""
        if 0x02 in self.current_simulated_values and 2 in self.current_simulated_values[0x02]:
            if self.current_simulated_values[0x02][2] == 7.0:
                self.current_simulated_values[0x02][2] = 13.0  # Listo para iniciar
                print("✅ [AUTO] Filtro colocado → Avanzando a estado 13 (Listo para iniciar)")

    # ====================== LECTURA DE ESTADO ======================

    def _handle_analog_read(self):
        header = b'\x12\xaa\x00'
        analog_payload = b''

        for group_code, var_id in ANALOG_MAP:
            value = self.current_simulated_values.get(group_code, {}).get(var_id, 0.0)
            
            # === NUEVA LÓGICA: DETECTAR ESTADO 7 ===
            if group_code == 0x02 and var_id == 2:   # primingProcessStatus
                status_code = int(value)
                self._auto_handle_filter_fill(status_code)

            if self.realistic_mode:
                if "Temp" in VARIABLES.get(group_code, {}).get(var_id, {}).get("name", ""):
                    value += random.uniform(-0.3, 0.3)
                elif "Cond" in VARIABLES.get(group_code, {}).get(var_id, {}).get("name", ""):
                    value += random.uniform(-0.05, 0.05)

            analog_payload += struct.pack('<d', float(value))

        self._send_response(header + analog_payload)

    def _send_response(self, payload: bytes):
        if not self.serial_port or not self.serial_port.is_open:
            return
        crc = crc16(payload)
        frame = payload + bytes([crc >> 8, crc & 0xFF])
        try:
            self.serial_port.write(frame)
        except:
            pass


    def _handle_boolean_read(self):
        """Genera y envía la respuesta booleana"""
        header = b'\x11\x11\x00'
        
        boolean_payload_bytes = [0] * 60
        if 0x01 in self.current_simulated_values:
            for i in range(60):
                if i in self.current_simulated_values[0x01]:
                    boolean_payload_bytes[i] = 1 if self.current_simulated_values[0x01][i] else 0

        payload = bytes(boolean_payload_bytes)
        self._send_response(header + payload)


    def _handle_boolean_write(self, command_data: bytes):
        if len(command_data) != 4:
            return
        address = command_data[2]
        value = command_data[3] != 0x00

        print(f"[SIMULATOR] WRITE BOOLEAN → ID {address} = {value}")

        if 0x01 in self.current_simulated_values and address in self.current_simulated_values[0x01]:
            info = self._get_var_info(0x01, address)
            if info.get("rw", True):
                self.current_simulated_values[0x01][address] = bool(value)
                self.request_led_update.emit(address, bool(value))
            else:
                print(f"[SIMULATOR] WRITE BOOLEAN ignorado (solo lectura) ID {address}")
        else:
            print(f"[SIMULATOR] WRITE BOOLEAN ignorado (ID no mapeado) {address}")

   
            
        # Respuesta de éxito
        response_payload = bytes([0x21, 0x11, address, 0xFF])
        self._send_response(response_payload)

    def _handle_double_write(self, command_data: bytes):
        """command_data debe ser de 11 bytes (sin CRC)"""
        if len(command_data) != 11:
            print(f"[SIMULATOR] Error longitud: {len(command_data)}")
            return

        group_byte = command_data[0]
        group_code = group_byte & 0x0F
        var_id = command_data[2]
        value = struct.unpack('<d', command_data[3:11])[0]

        print(f"[SIMULATOR] WRITE DOUBLE → Grupo 0x{group_code:02X} | ID {var_id} = {value:.4f}")

        # Actualizar valor interno
        if group_code in self.current_simulated_values and var_id in self.current_simulated_values[group_code]:
            info = self._get_var_info(group_code, var_id)
            if info.get("type") == "double" and info.get("rw", True):
                self.current_simulated_values[group_code][var_id] = self._coerce_value(group_code, var_id, value)
            else:
                print(f"[SIMULATOR] WRITE DOUBLE ignorado (tipo/rw no válido) G:0x{group_code:02X} ID:{var_id}")
        else:
            print(f"[SIMULATOR] WRITE DOUBLE ignorado (variable no mapeada) G:0x{group_code:02X} ID:{var_id}")

        # === RESPUESTA CORRECTA SEGÚN PROTOCOLO ===
        response_payload = bytes([group_byte, 0xAA, var_id, 0xFF])
        self._send_response(response_payload)

    @Slot(int, bool)
    def update_led_visuals(self, var_id: int, state: bool):
        if var_id in self.led_widgets:
            self.led_widgets[var_id].set_state(state)
            self.led_widgets[var_id].update() # Forzar repintado visual
    
    def log_message(self, message: str):
        """Muestra logs elegantes en la miniconsola interna."""
        timestamp = time.strftime("%H:%M:%S")
        self.console_display.append(f"[{timestamp}] {message}")

    def closeEvent(self, event):
        self.stop_serial()
        print("[SIMULATOR] Simulador cerrado.")
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Simulator()
    window.show()
    sys.exit(app.exec())
