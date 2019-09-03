insert into doctors (people_id)
select people_id
from people
order by people_id desc
limit (100);
