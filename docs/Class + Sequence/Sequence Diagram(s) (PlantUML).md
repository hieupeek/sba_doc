# Sequence Diagram(s) (PlantUML)

Tài liệu thiết kế Sơ đồ tương tác đối tượng (Sequence Diagrams) cho các Use Case cốt lõi thuộc 5 phân hệ của hệ thống HMS.
Thiết kế chuẩn phương pháp COMET & Visual Paradigm: Áp dụng đầy đủ stereotype `<<boundary>>` cho các trang giao diện, `<<control>>` cho Controller và Service, và `Database` cho tầng CSDL. Sử dụng phong cách thẩm mỹ Visual Paradigm với màu xanh Cyan #67C8FF, các khung `alt` điều kiện tiếng Anh in đậm màu đen, thể hiện luồng trao đổi thông điệp hoàn chỉnh từ Actor -> Boundary -> Control -> Database.

---

## 1. Mục 4.2: UC-02 User Login Flow

```plantuml
@startuml
skinparam shadowed false
autonumber 1 "0: "
hide footbox

skinparam participantBackgroundColor #67C8FF
skinparam participantBorderColor #000000
skinparam participantFontColor #000000
skinparam participantFontStyle bold

skinparam databaseBackgroundColor #67C8FF
skinparam databaseBorderColor #000000
skinparam databaseFontColor #000000

skinparam sequenceLifeLineBackgroundColor #67C8FF
skinparam sequenceLifeLineBorderColor #000000
skinparam sequenceArrowColor #000000

skinparam SequenceGroupFontColor #000000
skinparam SequenceGroupFontStyle bold
skinparam SequenceGroupHeaderFontColor #000000
skinparam SequenceGroupHeaderFontStyle bold
skinparam SequenceGroupBorderColor #000000
skinparam SequenceGroupBackgroundColor transparent

actor Staff
participant LoginPage <<boundary>>
participant AuthController <<control>>
participant AuthService <<control>>
database Database

Staff -> LoginPage : Select option to login & input credentials
activate LoginPage

LoginPage -> LoginPage : validateLoginForm()
activate LoginPage
deactivate LoginPage

LoginPage -> AuthController : requestLogin(loginDTO)
activate AuthController

AuthController -> AuthService : authenticate(loginDTO)
activate AuthService

AuthService -> Database : Query user by email
activate Database
Database --> AuthService : Return user record
deactivate Database

alt Valid credentials & Active account
    AuthService -> AuthService : verifyPasswordHash()
    activate AuthService
    deactivate AuthService

    AuthService -> AuthService : generateJwtToken(user)
    activate AuthService
    deactivate AuthService

    AuthService --> AuthController : returnAuthResponse(token, role)
    deactivate AuthService

    AuthController --> LoginPage : returnSuccess(token, userProfile)
    deactivate AuthController

    LoginPage -> LoginPage : storeTokenInMemory(token)
    activate LoginPage
    deactivate LoginPage

    LoginPage --> Staff : Redirect to Dashboard (by Role)
    deactivate LoginPage
else Invalid credentials or Inactive account
    activate AuthService
    AuthService --> AuthController : returnUnauthorizedError()
    deactivate AuthService
    activate AuthController
    AuthController --> LoginPage : returnErrorResponse(401)
    deactivate AuthController
    activate LoginPage
    LoginPage --> Staff : Display error ("Invalid email or password")
    deactivate LoginPage
end
@enduml
```

---

## 2. Mục 4.3: Room & Facility Management

### 2.1 UC-19 Update Housekeeping Status

```plantuml
@startuml
skinparam shadowed false
autonumber 1 "0: "
hide footbox

skinparam participantBackgroundColor #67C8FF
skinparam participantBorderColor #000000
skinparam participantFontColor #000000
skinparam participantFontStyle bold

skinparam databaseBackgroundColor #67C8FF
skinparam databaseBorderColor #000000
skinparam databaseFontColor #000000

skinparam sequenceLifeLineBackgroundColor #67C8FF
skinparam sequenceLifeLineBorderColor #000000
skinparam sequenceArrowColor #000000

skinparam SequenceGroupFontColor #000000
skinparam SequenceGroupFontStyle bold
skinparam SequenceGroupHeaderFontColor #000000
skinparam SequenceGroupHeaderFontStyle bold
skinparam SequenceGroupBorderColor #000000
skinparam SequenceGroupBackgroundColor transparent

actor HousekeepingStaff
participant HousekeepingBoardPage <<boundary>>
participant HousekeepingController <<control>>
participant HousekeepingService <<control>>
database Database

HousekeepingStaff -> HousekeepingBoardPage : Click "Mark Clean" (roomId, remarks)
activate HousekeepingBoardPage

HousekeepingBoardPage -> HousekeepingController : updateCleanliness(roomId, statusDTO)
activate HousekeepingController

HousekeepingController -> HousekeepingService : changeRoomCleanliness(roomId, statusDTO)
activate HousekeepingService

HousekeepingService -> Database : Query room by id
activate Database
Database --> HousekeepingService : Return room record
deactivate Database

alt Room found & Eligible for transition
    HousekeepingService -> Database : Update room status = 'CLEAN'
    activate Database
    Database --> HousekeepingService : Confirm 1 row updated
    deactivate Database

    HousekeepingService --> HousekeepingController : returnStatusSuccess(roomDTO)
    deactivate HousekeepingService

    HousekeepingController --> HousekeepingBoardPage : returnSuccessResponse(200)
    deactivate HousekeepingController

    HousekeepingBoardPage --> HousekeepingStaff : Display Success Toast ("Room marked as Clean")
    deactivate HousekeepingBoardPage
else Room not found or Invalid state
    activate HousekeepingService
    HousekeepingService --> HousekeepingController : returnErrorStatus(404 / 400)
    deactivate HousekeepingService
    activate HousekeepingController
    HousekeepingController --> HousekeepingBoardPage : returnErrorResponse()
    deactivate HousekeepingController
    activate HousekeepingBoardPage
    HousekeepingBoardPage --> HousekeepingStaff : Display Error Toast ("Failed to update status")
    deactivate HousekeepingBoardPage
end
@enduml
```

---

### 2.2 UC-20 Set Room Maintenance

```plantuml
@startuml
skinparam shadowed false
autonumber 1 "0: "
hide footbox

skinparam participantBackgroundColor #67C8FF
skinparam participantBorderColor #000000
skinparam participantFontColor #000000
skinparam participantFontStyle bold

skinparam databaseBackgroundColor #67C8FF
skinparam databaseBorderColor #000000
skinparam databaseFontColor #000000

skinparam sequenceLifeLineBackgroundColor #67C8FF
skinparam sequenceLifeLineBorderColor #000000
skinparam sequenceArrowColor #000000

skinparam SequenceGroupFontColor #000000
skinparam SequenceGroupFontStyle bold
skinparam SequenceGroupHeaderFontColor #000000
skinparam SequenceGroupHeaderFontStyle bold
skinparam SequenceGroupBorderColor #000000
skinparam SequenceGroupBackgroundColor transparent

actor HousekeepingStaff
participant SetMaintenancePage <<boundary>>
participant MaintenanceController <<control>>
participant MaintenanceService <<control>>
database Database

HousekeepingStaff -> SetMaintenancePage : Submit Maintenance Form (roomId, defect, date)
activate SetMaintenancePage

SetMaintenancePage -> MaintenanceController : createMaintenance(roomId, maintenanceDTO)
activate MaintenanceController

MaintenanceController -> MaintenanceService : scheduleMaintenance(roomId, maintenanceDTO)
activate MaintenanceService

MaintenanceService -> Database : Query room & occupancy status
activate Database
Database --> MaintenanceService : Return room details
deactivate Database

alt Room is vacant (No active stay)
    MaintenanceService -> Database : Save maintenance record & lock room status ('UNDER_MAINTENANCE')
    activate Database
    Database --> MaintenanceService : Confirm maintenance scheduled
    deactivate Database

    MaintenanceService --> MaintenanceController : returnMaintenanceResponse(dto)
    deactivate MaintenanceService

    MaintenanceController --> SetMaintenancePage : returnCreatedSuccess(201)
    deactivate MaintenanceController

    SetMaintenancePage --> HousekeepingStaff : Display Success Toast ("Room locked for Maintenance")
    deactivate SetMaintenancePage
else Room is currently occupied
    activate MaintenanceService
    MaintenanceService --> MaintenanceController : returnOccupiedConflictError(400)
    deactivate MaintenanceService
    activate MaintenanceController
    MaintenanceController --> SetMaintenancePage : returnErrorResponse(400)
    deactivate MaintenanceController
    activate SetMaintenancePage
    SetMaintenancePage --> HousekeepingStaff : Display Error ("Cannot set maintenance for occupied room")
    deactivate SetMaintenancePage
end
@enduml
```

---

## 3. Mục 4.4: Reservation & Front-Desk Operations

### 3.1 UC-23 Room Reservation

```plantuml
@startuml
skinparam shadowed false
autonumber 1 "0: "
hide footbox

skinparam participantBackgroundColor #67C8FF
skinparam participantBorderColor #000000
skinparam participantFontColor #000000
skinparam participantFontStyle bold

skinparam databaseBackgroundColor #67C8FF
skinparam databaseBorderColor #000000
skinparam databaseFontColor #000000

skinparam sequenceLifeLineBackgroundColor #67C8FF
skinparam sequenceLifeLineBorderColor #000000
skinparam sequenceArrowColor #000000

skinparam SequenceGroupFontColor #000000
skinparam SequenceGroupFontStyle bold
skinparam SequenceGroupHeaderFontColor #000000
skinparam SequenceGroupHeaderFontStyle bold
skinparam SequenceGroupBorderColor #000000
skinparam SequenceGroupBackgroundColor transparent

actor Customer
participant BookingPage <<boundary>>
participant ReservationController <<control>>
participant ReservationService <<control>>
database Database

Customer -> BookingPage : Fill guest info, dates & click "Confirm Booking"
activate BookingPage

BookingPage -> ReservationController : createReservation(bookingDTO)
activate ReservationController

ReservationController -> ReservationService : processBooking(bookingDTO)
activate ReservationService

ReservationService -> Database : Check room availability quota for dates & category
activate Database
Database --> ReservationService : Return availability count
deactivate Database

alt Room quota available for interval
    ReservationService -> Database : Save reservation transaction (customer, reservation & details)
    activate Database
    Database --> ReservationService : Confirm reservation saved (bookingRef)
    deactivate Database

    ReservationService -> ReservationService : dispatchConfirmationEmail(booking)
    activate ReservationService
    deactivate ReservationService

    ReservationService --> ReservationController : returnReservationSuccess(bookingRef)
    deactivate ReservationService

    ReservationController --> BookingPage : returnCreatedSuccess(201, bookingRef)
    deactivate ReservationController

    BookingPage --> Customer : Display Booking Confirmation ("Booking #HMS-9021 confirmed")
    deactivate BookingPage
else Room category fully booked
    activate ReservationService
    ReservationService --> ReservationController : returnQuotaExceededError(409)
    deactivate ReservationService
    activate ReservationController
    ReservationController --> BookingPage : returnConflictResponse(409)
    deactivate ReservationController
    activate BookingPage
    BookingPage --> Customer : Display Notification ("Fully booked, please select other dates")
    deactivate BookingPage
end
@enduml
```

---

### 3.2 UC-27 Guest Check-in

```plantuml
@startuml
skinparam shadowed false
autonumber 1 "0: "
hide footbox

skinparam participantBackgroundColor #67C8FF
skinparam participantBorderColor #000000
skinparam participantFontColor #000000
skinparam participantFontStyle bold

skinparam databaseBackgroundColor #67C8FF
skinparam databaseBorderColor #000000
skinparam databaseFontColor #000000

skinparam sequenceLifeLineBackgroundColor #67C8FF
skinparam sequenceLifeLineBorderColor #000000
skinparam sequenceArrowColor #000000

skinparam SequenceGroupFontColor #000000
skinparam SequenceGroupFontStyle bold
skinparam SequenceGroupHeaderFontColor #000000
skinparam SequenceGroupHeaderFontStyle bold
skinparam SequenceGroupBorderColor #000000
skinparam SequenceGroupBackgroundColor transparent

actor Receptionist
participant CheckInPage <<boundary>>
participant FrontDeskController <<control>>
participant FrontDeskService <<control>>
database Database

Receptionist -> CheckInPage : Input Booking Code & click "Check-in Guest"
activate CheckInPage

CheckInPage -> FrontDeskController : checkInGuest(checkInDTO)
activate FrontDeskController

FrontDeskController -> FrontDeskService : performCheckIn(checkInDTO)
activate FrontDeskService

FrontDeskService -> Database : Query reservation & available clean rooms
activate Database
Database --> FrontDeskService : Return reservation details & room list
deactivate Database

alt Valid booking & Clean room available
    FrontDeskService -> Database : Save check-in transaction (create stay, assignment & set status 'OCCUPIED')
    activate Database
    Database --> FrontDeskService : Confirm check-in transaction committed
    deactivate Database

    FrontDeskService --> FrontDeskController : returnCheckInResponse(roomKey, stayDetails)
    deactivate FrontDeskService

    FrontDeskController --> CheckInPage : returnSuccessResponse(200)
    deactivate FrontDeskController

    CheckInPage --> Receptionist : Display Check-in Success & Print RFID Key Card
    deactivate CheckInPage
else Booking not found or No clean room ready
    activate FrontDeskService
    FrontDeskService --> FrontDeskController : returnCheckInError(400)
    deactivate FrontDeskService
    activate FrontDeskController
    FrontDeskController --> CheckInPage : returnErrorResponse(400)
    deactivate FrontDeskController
    activate CheckInPage
    CheckInPage --> Receptionist : Display Error ("No clean room available for assignment")
    deactivate CheckInPage
end
@enduml
```

---

## 4. Mục 4.5: UC-37 & UC-39 Check-out & Payment Settlement

```plantuml
@startuml
skinparam shadowed false
autonumber 1 "0: "
hide footbox

skinparam participantBackgroundColor #67C8FF
skinparam participantBorderColor #000000
skinparam participantFontColor #000000
skinparam participantFontStyle bold

skinparam databaseBackgroundColor #67C8FF
skinparam databaseBorderColor #000000
skinparam databaseFontColor #000000

skinparam sequenceLifeLineBackgroundColor #67C8FF
skinparam sequenceLifeLineBorderColor #000000
skinparam sequenceArrowColor #000000

skinparam SequenceGroupFontColor #000000
skinparam SequenceGroupFontStyle bold
skinparam SequenceGroupHeaderFontColor #000000
skinparam SequenceGroupHeaderFontStyle bold
skinparam SequenceGroupBorderColor #000000
skinparam SequenceGroupBackgroundColor transparent

actor Cashier
participant BillingPage <<boundary>>
participant BillingController <<control>>
participant BillingService <<control>>
database Database

Cashier -> BillingPage : Click "Settle Payment & Check-out" (stayId, method)
activate BillingPage

BillingPage -> BillingController : processCheckOutPayment(settlementDTO)
activate BillingController

BillingController -> BillingService : settleFolioAndCheckout(settlementDTO)
activate BillingService

BillingService -> Database : Query folio, charges & service orders by stayId
activate Database
Database --> BillingService : Return folio summary
deactivate Database

BillingService -> BillingService : calculateGrandTotal(charges, services, taxes)
activate BillingService
deactivate BillingService

alt Payment authorized & Card approved
    BillingService -> Database : Save payment & close folio transaction (create invoice, payment & mark room 'DIRTY')
    activate Database
    Database --> BillingService : Confirm folio settlement committed
    deactivate Database

    BillingService --> BillingController : returnInvoiceReceipt(receiptData)
    deactivate BillingService

    BillingController --> BillingPage : returnSuccessResponse(200)
    deactivate BillingController

    BillingPage --> Cashier : Display Receipt Modal & Trigger Print
    deactivate BillingPage
else Payment declined or Insufficient funds
    activate BillingService
    BillingService --> BillingController : returnPaymentDeclinedError(400)
    deactivate BillingService
    activate BillingController
    BillingController --> BillingPage : returnErrorResponse(400)
    deactivate BillingController
    activate BillingPage
    BillingPage --> Cashier : Display Error ("Payment declined, request alternative method")
    deactivate BillingPage
end
@enduml
```

---

## 5. Mục 4.6: UC-46 Generate Revenue Analytics Report

```plantuml
@startuml
skinparam shadowed false
autonumber 1 "0: "
hide footbox

skinparam participantBackgroundColor #67C8FF
skinparam participantBorderColor #000000
skinparam participantFontColor #000000
skinparam participantFontStyle bold

skinparam databaseBackgroundColor #67C8FF
skinparam databaseBorderColor #000000
skinparam databaseFontColor #000000

skinparam sequenceLifeLineBackgroundColor #67C8FF
skinparam sequenceLifeLineBorderColor #000000
skinparam sequenceArrowColor #000000

skinparam SequenceGroupFontColor #000000
skinparam SequenceGroupFontStyle bold
skinparam SequenceGroupHeaderFontColor #000000
skinparam SequenceGroupHeaderFontStyle bold
skinparam SequenceGroupBorderColor #000000
skinparam SequenceGroupBackgroundColor transparent

actor Manager
participant RevenueAnalyticsPage <<boundary>>
participant ReportController <<control>>
participant ReportService <<control>>
database Database

Manager -> RevenueAnalyticsPage : Select Date Range & click "Generate Revenue Report"
activate RevenueAnalyticsPage

RevenueAnalyticsPage -> ReportController : getRevenueAnalytics(fromDate, toDate)
activate ReportController

ReportController -> ReportService : generateRevenueReport(fromDate, toDate)
activate ReportService

alt Valid date interval (From Date <= To Date)
    ReportService -> Database : Query revenue & occupancy datasets for period
    activate Database
    Database --> ReportService : Return revenue & occupancy summary
    deactivate Database

    ReportService -> ReportService : compileSummaryKPIs(totalRev, adr, revPAR, occupancyPct)
    activate ReportService
    deactivate ReportService

    ReportService --> ReportController : returnRevenueReport(kpiDTO, chartData)
    deactivate ReportService

    ReportController --> RevenueAnalyticsPage : returnSuccessResponse(200, chartData)
    deactivate ReportController

    RevenueAnalyticsPage -> RevenueAnalyticsPage : renderChartsAndKPICards()
    activate RevenueAnalyticsPage
    deactivate RevenueAnalyticsPage

    RevenueAnalyticsPage --> Manager : Display Revenue Dashboard & Enable PDF Export
    deactivate RevenueAnalyticsPage
else Invalid date range (From Date > To Date)
    activate ReportService
    ReportService --> ReportController : returnInvalidDateError(400)
    deactivate ReportService
    activate ReportController
    ReportController --> RevenueAnalyticsPage : returnErrorResponse(400)
    deactivate ReportController
    activate RevenueAnalyticsPage
    RevenueAnalyticsPage --> Manager : Display Error ("From Date must be prior to To Date")
    deactivate RevenueAnalyticsPage
end
@enduml
```

---
