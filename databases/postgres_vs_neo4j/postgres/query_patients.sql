select p.people_id as patient_id
, concat(p.first_name, ' ', p.last_name) as patient
, concat(d.first_name, ' ', d.last_name) as doctor
, i.name as illness
, t.name as treatments
from people p
inner join patients_doctors pd
on p.people_id = pd.people_id
inner join people d
on pd.doctor_id = d.people_id
inner join patients_illnesses p_ill
on p_ill.people_id = p.people_id
inner join illnesses i
on i.illness_id = p_ill.illness_id
inner join illness_treatment it
on it.illness_id = i.illness_id
inner join treatments t
on t.treatment_id = it.treatment_id;
