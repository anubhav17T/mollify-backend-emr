from fastapi import status


class ConsultationStatusMessage:
    def __init__(self, status: str, id: int):
        self.status = status
        self.id = id

    def message(self):
        if self.status is None:
            return {"message": "CHEERS!! Your consultation has been booked",
                    "code": status.HTTP_201_CREATED,
                    "id": self.id,
                    "success": True}

        if self.status == "OPEN":
            return {"message": "CHEERS!! Your consultation has been booked",
                    "code": status.HTTP_201_CREATED,
                    "id": self.id,
                    "success": True}

        if self.status == "INPROGRESS":
            return {"message": "Now Your consultation Is In Progress,have a great session (Note:- ConsultationCannot "
                               "be cancelled)",
                    "code": status.HTTP_200_OK,
                    "id": self.id,
                    "success": True}

        if self.status == "COMPLETED":
            return {"message": "CONGRATULATIONS !! Your consultations has been completed successfully",
                    "code": status.HTTP_200_OK,
                    "id": self.id,
                    "success": True}

        if self.status == "CANCELLED":
            return {"message": "Your Consultation has been cancelled, amount will be refunded in 3-5 days",
                    "code": status.HTTP_200_OK,
                    "id": self.id,
                    "success": True}

        if self.status == "RESCHEDULED":
            return {"message": "Your Confirmation has been rescheduled to your preferable time",
                    "code": status.HTTP_200_OK,
                    "id": self.id,
                    "success": True}
