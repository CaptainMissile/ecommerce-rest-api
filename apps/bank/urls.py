from django.urls import path

from .views import (BankAccountCreateAPI,BankAccountUpdateAPI,
                    BankAccountDeleteAPI,BankAccountSingleAPI,
                    BankAccountListAPI, 
                    AddMoneyToAccountRequestAPI,
                    SendMoneyToAccountRequestAPI,
                    TransactionSingleAPI,
                    TransactionListAPI,
                    TransactionFilterAPI,
                    ApproveCashInRequestAPI,
                    ApproveSendMoneyRequestAPI)


app_name = 'bank'

urlpatterns = [
    path('create-account/', BankAccountCreateAPI.as_view(), name='create_account'),
    path('update-account/<int:account_no>', BankAccountUpdateAPI.as_view(), name="update_account"),
    path('delete-account/<int:account_no>', BankAccountDeleteAPI.as_view(), name='delete_account'),
    path('single-account/<int:account_no>', BankAccountSingleAPI.as_view(), name="single-account"),
    path('list-account/', BankAccountListAPI.as_view(), name="list-account"),


    path('single-transaction/', TransactionSingleAPI.as_view(), name="single-transaction"),
    path('list-transaction/', TransactionListAPI.as_view(), name="list_transaction"),
    path('filter-transaction/', TransactionFilterAPI.as_view(), name="filter_transaction"),
    path('add-money-request/', AddMoneyToAccountRequestAPI.as_view(), name="add_money_request"),
    path('send-money-request/', SendMoneyToAccountRequestAPI.as_view(), name="send_money_request"),
    path('approve-cash-in-request/<int:transaction_id>', ApproveCashInRequestAPI.as_view(), name="approve_cash_in_request"),
    path('approve-send-money-request/<int:transaction_id>', ApproveSendMoneyRequestAPI.as_view(), name="approve_send_money_request")
]
