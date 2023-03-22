from app.sdk import ActionRequest, ActionResponse

request = ActionRequest(query="Test request", variables={"x": 1})


def action(request: ActionRequest) -> ActionResponse:
    request.variables["test"] = "success"
    return ActionResponse(message=request.query, variables=request.variables)
