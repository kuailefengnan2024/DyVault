Vector3 targetDirection = target.position - transform.position;
Quaternion rotation = Quaternion.LookRotation(targetDirection, Vector3.up);
transform.rotation = rotation;