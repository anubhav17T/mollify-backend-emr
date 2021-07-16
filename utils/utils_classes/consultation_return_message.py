from fastapi import status


class ConsultationStatusMessage:
    def __init__(self, status: str):
        self.status = status

    def message(self):
        if self.status == "OPEN":
            return {"message": "CHEERS!! Your consultation has been booked",
                    "code": status.HTTP_201_CREATED,
                    "success": True}

        if self.status == "INPROGRESS":
            return {"message": "Now Your consultation Is In Progress,have a great session (Note:- ConsultationCannot "
                               "be cancelled)",
                    "code": status.HTTP_200_OK,
                    "success": True}

        if self.status == "COMPLETED":
            return {"message": "CONGRATULATIONS !! Your consultations has been completed successfully",
                    "code": status.HTTP_200_OK,
                    "success": True}

        if self.status == "CANCELLED":
            return {"message": "We Regret that you have cancelled the confirmation",
                    "code": status.HTTP_200_OK,
                    "success": True}

        if self.status == "RESCHEDULED":
            return {"message": "Your Confirmation has been rescheduled to your preferrable time",
                    "code": status.HTTP_200_OK,
                    "success": True}
