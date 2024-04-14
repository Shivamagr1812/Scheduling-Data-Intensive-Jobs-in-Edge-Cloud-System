def schedule(C, NTS_rd):
    # Sort C based on the remaining number of required time slots for d in ascending order
    C.sort(key=lambda x: x[1])  # Assuming each chunk in C is represented as (chunk_id, remaining_time_slots)

    for chunk_index in range(len(C)):
        chunk_id, remaining_time_slots = C[chunk_index]

        # Check if remaining time slots of the chunk is greater than 0
        if remaining_time_slots - NTS_rd > 0:
            # Update remaining time slots and NTS_rd
            remaining_time_slots -= NTS_rd
            NTS_rd = 0
            C[chunk_index] = (chunk_id, remaining_time_slots)  # Update the remaining time slots in the original list
            break
        else:
            # Update NTS_rd and set remaining time slots to 0
            NTS_rd -= remaining_time_slots
            C[chunk_index] = (chunk_id, 0)  # Set remaining time slots to 0 in the original list
            # Remove the chunk from the original list C
            C.pop(chunk_index)
            break

    return C, NTS_rd