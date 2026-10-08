import logging
import random
import smtplib
from email.message import EmailMessage
print("=============================")
print("     TANKE SMART SAFETY      ")
print("=============================")



logging.basicConfig(format="%(asctime)s - %(message)s")
def monitor_event(station_id, temperature, status, customer):
    if status == "critical":
            logging.critical(
            f"CRITICAL ALERT: Station {station_id} reached {temperature}°C! "
            f"Charging stopped."
        )
            message = message = f"""
            Dear {customer["name"]},

            a critical temperature has been detected at the TankE charging station.

            Station: {station_id}
            Temperature: {temperature:.1f} °C
            Status: CRITICAL

            For safety reasons, the charging process has been stopped automatically.

            No further action is required from you at this moment.

            Best regards,
            TankE Smart Safety Monitor
            Automated Safety System
            """
            send_email(customer["email"], message)
            notify_technical_service(station_id, message)
    
    elif status == "normal":
        logging.info("Your car is charging")
    elif status == "warning":
        logging.warning(f"warning station {station_id} reached {temperature}°C!")


def send_email(owner, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("YOUR_EMAIL@gmail.com", "")
    email = EmailMessage()
    email["From"] = "YOUR_EMAIL@gmail.com"
    email["To"] = owner
    email["Subject"] = "⚠️ TankE Safety Alert - Charging stopped"
    email.set_content(message)
    server.send_message(email)
    server.quit()
def notify_technical_service(station, message):
    print(f'{message} is sent to {station}')


#asking the user for his informations
while True:
    name = input("Name: ").strip()
    email = input("E-Mail: ").strip()
    phone = input("Telefonnummer: ").strip()

    if name.replace(" ", "").isalpha() and "@" in email and phone.isdigit():
        print("Kontaktdaten erhalten.")
        break
    else:
        print("Bitte geben Sie gültige Kontaktdaten ein.")

customer = {"name":name, "email":email, "phone":phone}


#asking for charging infos
while True:
    station=input("TankE-Ladestation Nummer: ").strip()
    if station != "":
        break
    else :
        print("Bitte eine Ladestationsnummer eingeben.")

#detecting the car type 
while True:
    car_type = input("Fahrzeugtyp (kleinwagen, Mittelklasse, SUV): ").strip()

    if car_type in ["kleinwagen", "Mittelklasse", "SUV"]:
        break
    else:
        print("Bitte einen gültigen Fahrzeugtyp eingeben.")


#determine charging power 

charging_power=0
if car_type =="kleinwagen":
    charging_power=random.choice([7,11])

elif car_type == "Mittelklasse":
    charging_power = random.choice([11, 22])

elif car_type == "SUV":
    charging_power = random.choice([11, 22])   

print(f"Ladeleistung: {charging_power} kW")

if car_type == "kleinwagen":
    battery_capacity = 40
elif car_type == "Mittelklasse":
    battery_capacity = 60
elif car_type == "SUV":
    battery_capacity = 80


#Now we need the car's current battery percentage:
while True:
    try:
        Batterie=float(input("Auto Batteriestand in %:"))
        if  0<Batterie<100 :
            break
        else :
            print("Der batteriestand muss zwischen 0 und 100 sein ")
    except ValueError :
        print("Bitte eine gültige Zahl eingeben")

remaining_percentage = 100 - Batterie
energy_needed = battery_capacity * (remaining_percentage/100)
charging_hours = energy_needed/charging_power
charging_time_needed = charging_hours*60



#check the actual TankE temperature:


session_type = random.choices(
    ["normal", "warning", "critical"],
    weights=[50, 30, 20]
)[0]

temperature = random.uniform(25, 40)
print(f"Temperatur der Ladestation:{temperature:.1f}°C")


#charging time 
charging_time = 0
power_reduced = False
warning_printed = False
charging_stopped = False

while charging_time < charging_time_needed:
    charging_time += 1

    # temperature changes
    if session_type == "normal":
        temperature += random.uniform(-0.25, 0.5)

    elif session_type == "warning":
        temperature += random.uniform(0.5, 2.0)

    elif session_type == "critical":
        temperature += random.uniform(1.5, 3.0)

    # check temperature
    if temperature >= 60:
        session_status = "critical"

    elif temperature >= 50:
        session_status = "warning"

    else:
        session_status = "normal"

    monitor_event(station, temperature, session_status, customer)


# now time for the system reaction   

    if session_status == "critical":
        print("KRITISCH: Laden wird sofort gestoppt.")
        charging_stopped = True
        break

    elif session_status == "warning" and warning_printed == False:
        print("WARNUNG: Temperatur ist erhöht.")
        warning_printed = True
  
    else:
        pass
# react to warm temperature
    
    if session_status == "warning" and power_reduced == False:
        charging_power = charging_power / 2
        power_reduced = True


#calculate the energy charged 

charging_hours = charging_time / 60
energy_charged = charging_power * charging_hours

print(f"Ladezeit: {charging_time} Minuten")
print(f"Geladene Energie: {energy_charged:.2f} kWh")

if charging_stopped:
    print("Grund: Sicherheitsabschaltung")
else:
    print("Grund: Ladevorgang nach 60 Minuten beendet")


