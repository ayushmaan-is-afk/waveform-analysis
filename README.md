<font size=5> 
______  _____ _________  ___  _    _  ___  _   _ ___________ ______________  ___   ___   _   _   ___   _   __   _______ _____ _____ 
|  _  \/  __ \| ___ \  \/  | | |  | |/ _ \| | | |  ___|  ___|  _  | ___ \  \/  |  / _ \ | \ | | / _ \ | |  \ \ / /  ___|_   _/  ___|
| | | || /  \/| |_/ / .  . | | |  | / /_\ \ | | | |__ | |_  | | | | |_/ / .  . | / /_\ \|  \| |/ /_\ \| |   \ V /\ `--.  | | \ `--. 
| | | || |    |    /| |\/| | | |/\| |  _  | | | |  __||  _| | | | |    /| |\/| | |  _  || . ` ||  _  || |    \ /  `--. \ | |  `--. \
| |/ / | \__/\| |\ \| |  | | \  /\  / | | \ \_/ / |___| |   \ \_/ / |\ \| |  | | | | | || |\  || | | || |____| | /\__/ /_| |_/\__/ /
|___/   \____/\_| \_\_|  |_/  \/  \/\_| |_/\___/\____/\_|    \___/\_| \_\_|  |_/ \_| |_/\_| \_/\_| |_/\_____/\_/ \____/ \___/\____/ 
                                                                                                                                    
                                                                                                                                    
  </font>
**DCRM Anomaly detection using Machine Learning**. 

DCRM is a test conducted to assess the condition of Extra-High Volatge Circuit Breakers. This test is done every 2-3 years, depending on the substation.
The test result is usually in the form of a waveform graph or raw data. 

What our project does? 

- Using ISOLATION FOREST decision tree, we aim to mitigate human errors in the process of analysing the test results. 
Trained on a proprietary dataset provided by the M.O.P., the model is able to predict the smallest of anomalies and provides the user with metrics such as -
1. Status of the Circuit Breaker
2. Severity(in case of damages)
3. Anomaly Score
4. Anomaly percentage  
and several other statistics. 

Upcoming features - 
1. 1-D CNN to be able to read and predict from waveform graphs. 
2. More accuracy and robustness with autoencoder(s).
3. Authentication.
4. Predictive maintainance information.

Main deliverables - 

1. Anomaly detection.
2. Specify the faulty parts with faults. 
3. Predict failure prone parts.
4. Predict the type of failure. ex. arc-wear, contact-wear, etc.
 
 
The data on which the model was trained on contained these columns-
[
    'Coil Current C1 (A)', 'Coil Current C2 (A)', 'Coil Current C3 (A)',
    'Coil Current C4 (A)', 'Coil Current C5 (A)', 'Coil Current C6 (A)',
    'Contact Travel T1 (mm)', 'Contact Travel T2 (mm)',
    'Contact Travel T3 (mm)', 'Contact Travel T4 (mm)',
    'Contact Travel T5 (mm)', 'Contact Travel T6 (mm)',
    'DCRM Res CH1 in uOhm', 'DCRM Current CH1 in Amp',
    'CH1 Close-Velocity (m/s)', 'CH1 Open-Velocity (m/s)', 'CH1 Test Run',
    'DCRM Res CH2 in uOhm', 'DCRM Current CH2 in Amp',
    'CH2 Close-Velocity (m/s)', 'CH2 Open-Velocity (m/s)', 'CH2 Test Run',
    'DCRM Res CH3 in uOhm', 'DCRM Current CH3 in Amp',
    'CH3 Close-Velocity (m/s)', 'CH3 Open-Velocity (m/s)', 'CH3 Test Run',
    'DCRM Res CH4 in uOhm', 'DCRM Current CH4 in Amp',
    'CH4 Close-Velocity (m/s)', 'CH4 Open-Velocity (m/s)', 'CH4 Test Run',
    'DCRM Res CH5 in uOhm', 'DCRM Current CH5 in Amp',
    'CH5 Close-Velocity (m/s)', 'CH5 Open-Velocity (m/s)', 'CH5 Test Run',
    'DCRM Res CH6 in uOhm', 'DCRM Current CH6 in Amp',
    'CH6 Close-Velocity (m/s)', 'CH6 Open-Velocity (m/s)', 'CH6 Test Run',
    'phase', 'CH3 Resistance Break', 'CH4 Resistance Break',
    'CH3 Bounce Break', 'CH4 Bounce Break', 'breaker_id',
    'CH1 Resistance Break', 'CH2 Resistance Break', 'CH1 Bounce Break',
    'CH2 Bounce Break'
],


Made with ❤️ by Ayushmaan Bhatnagar
