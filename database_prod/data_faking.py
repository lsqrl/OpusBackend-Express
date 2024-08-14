new_retail_record = Retail(
    name="Alice Smith",
    onboarding_datetime=datetime.strptime('2024-07-23T14:20:00', '%Y-%m-%dT%H:%M:%S'),
    email="alice.smith@gmail.com",
    telephone_number="+1-123-45-67",
    address_of_residence="217 W Dunklin Street, Jefferson City, MO 65101",
    country_of_residence="United States of America",
    citizenship="United States of America",
    gender="Female",
    birth_date=date(1990, 5, 15),  # Using a specific date format (YYYY-MM-DD)
    ssn="123-45-6789",
    dossier_id="D-0001"
)

# Add the record to the session and commit it to the database
session.add(new_retail_record)
session.commit()



new_legal_entity_record = LegalEntity(
    legal_entity_name="Lemma Finance Ltd",
    onboarding_datetime=datetime.strptime('2024-07-23T14:20:00', '%Y-%m-%dT%H:%M:%S'),
    email="support@lemma.io",
    telephone_number="+41 12345678",
    legal_address="4 Times Square, New York, NY 12345",
    country_of_incorporation="United States of America",
    dossier_id="6523416"
)

# Add the record to the session and commit it to the database
session.add(new_legal_entity_record)
session.commit()



new_account = Account(id=None, counterparty_id=12345, counterparty_type='Broker', type_id=1, 
        opening_time='2024-08-14 00:00:00', active=True, closing_time='2999-12-31 00:00:00', trade_enabled=True)