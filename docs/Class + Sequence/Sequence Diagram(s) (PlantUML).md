# Sequence Diagram(s) (PlantUML)

Tài liệu thiết kế Sơ đồ tương tác đối tượng (Sequence Diagrams) cho các Use Case cốt lõi thuộc 5 phân hệ của hệ thống HMS.
Tuân thủ tiêu chuẩn: Đánh số `autonumber 1 "0 : "`, Actor dạng người, tất cả các thành phần hệ thống đều dùng `participant` hình hộp chữ nhật, thể hiện đầy đủ self-call, activation bar và mũi tên nét đứt (`-->`) phản hồi.

---

## 1. Mục 4.2: UC-02 User Login Flow

```plantuml
@startuml
skinparam shadowed false
autonumber 1 "0 : "

actor "Lifeline2: User" as User
participant LoginPage
participant ApiClient
participant JwtAuthenticationFilter
participant AuthenticationController
participant AuthenticationServiceImpl
participant UserRepository
participant JwtTokenProvider

User -> LoginPage : Input username & password, click "Login"
activate LoginPage

LoginPage -> LoginPage : validateLoginForm
activate LoginPage
deactivate LoginPage

LoginPage -> ApiClient : post("/api/v1/auth/login", loginDTO)
activate ApiClient

ApiClient -> JwtAuthenticationFilter : HTTP POST /api/v1/auth/login
activate JwtAuthenticationFilter

JwtAuthenticationFilter -> AuthenticationController : login(loginDTO)
deactivate JwtAuthenticationFilter
activate AuthenticationController

AuthenticationController -> AuthenticationServiceImpl : authenticate(loginDTO)
activate AuthenticationServiceImpl

AuthenticationServiceImpl -> UserRepository : findByEmail(email)
activate UserRepository
UserRepository --> AuthenticationServiceImpl : return User entity
deactivate UserRepository

AuthenticationServiceImpl -> AuthenticationServiceImpl : verifyPasswordHash(raw, hashed)
activate AuthenticationServiceImpl
deactivate AuthenticationServiceImpl

AuthenticationServiceImpl -> JwtTokenProvider : generateToken(user)
activate JwtTokenProvider
JwtTokenProvider --> AuthenticationServiceImpl : return jwtAccessToken
deactivate JwtTokenProvider

AuthenticationServiceImpl --> AuthenticationController : return AuthResponseDTO(token, role)
deactivate AuthenticationServiceImpl

AuthenticationController --> ApiClient : HTTP 200 OK (JWT, UserProfile)
deactivate AuthenticationController

ApiClient --> LoginPage : Promise resolved
deactivate ApiClient

LoginPage -> LoginPage : storeTokenInMemory(token)
activate LoginPage
deactivate LoginPage

LoginPage --> User : Redirect to Dashboard (by Role)
deactivate LoginPage
@enduml
```

---

## 2. Mục 4.3: Room & Facility Management

### 2.1 UC-19 Update Housekeeping Status
```plantuml
@startuml
skinparam shadowed false
autonumber 1 "0 : "

actor "Lifeline2: Housekeeping Staff" as HKStaff
participant HousekeepingBoardView
participant ApiClient
participant JwtAuthenticationFilter
participant HousekeepingController
participant HousekeepingServiceImpl
participant RoomRepository

HKStaff -> HousekeepingBoardView : Click "Mark Clean" (roomId, remarks)
activate HousekeepingBoardView

HousekeepingBoardView -> ApiClient : put("/api/v1/housekeeping/rooms/{id}/cleanliness", dto)
activate ApiClient

ApiClient -> JwtAuthenticationFilter : HTTP PUT with Bearer Token
activate JwtAuthenticationFilter

JwtAuthenticationFilter -> JwtAuthenticationFilter : validateJwtToken()
activate JwtAuthenticationFilter
deactivate JwtAuthenticationFilter

JwtAuthenticationFilter -> HousekeepingController : updateCleanliness(roomId, dto)
deactivate JwtAuthenticationFilter
activate HousekeepingController

HousekeepingController -> HousekeepingServiceImpl : changeRoomCleanliness(roomId, dto)
activate HousekeepingServiceImpl

HousekeepingServiceImpl -> RoomRepository : findById(roomId)
activate RoomRepository
RoomRepository --> HousekeepingServiceImpl : return Room entity
deactivate RoomRepository

HousekeepingServiceImpl -> HousekeepingServiceImpl : verifyTransitionEligibility()
activate HousekeepingServiceImpl
deactivate HousekeepingServiceImpl

HousekeepingServiceImpl -> RoomRepository : save(updatedRoom)
activate RoomRepository
RoomRepository --> HousekeepingServiceImpl : return persisted Room
deactivate RoomRepository

HousekeepingServiceImpl --> HousekeepingController : return RoomStatusResponseDTO
deactivate HousekeepingServiceImpl

HousekeepingController --> ApiClient : HTTP 200 OK (JSON)
deactivate HousekeepingController

ApiClient --> HousekeepingBoardView : Promise resolved
deactivate ApiClient

HousekeepingBoardView --> HKStaff : Display Success Toast ("Room marked as Clean")
deactivate HousekeepingBoardView
@enduml
```

### 2.2 UC-20 Set Room Maintenance
```plantuml
@startuml
skinparam shadowed false
autonumber 1 "0 : "

actor "Lifeline2: Housekeeping Staff" as HKStaff
participant SetMaintenanceView
participant ApiClient
participant JwtAuthenticationFilter
participant RoomMaintenanceController
participant RoomMaintenanceServiceImpl
participant RoomRepository
participant RoomMaintenanceRepository

HKStaff -> SetMaintenanceView : Submit Maintenance Form (roomId, defect, date)
activate SetMaintenanceView

SetMaintenanceView -> ApiClient : post("/api/v1/maintenance/rooms/{id}", dto)
activate ApiClient

ApiClient -> JwtAuthenticationFilter : HTTP POST with Bearer Token
activate JwtAuthenticationFilter

JwtAuthenticationFilter -> RoomMaintenanceController : createMaintenance(roomId, dto)
deactivate JwtAuthenticationFilter
activate RoomMaintenanceController

RoomMaintenanceController -> RoomMaintenanceServiceImpl : scheduleMaintenance(roomId, dto)
activate RoomMaintenanceServiceImpl

RoomMaintenanceServiceImpl -> RoomRepository : findById(roomId)
activate RoomRepository
RoomRepository --> RoomMaintenanceServiceImpl : return Room entity
deactivate RoomRepository

RoomMaintenanceServiceImpl -> RoomMaintenanceServiceImpl : checkOccupancyStatus(room)
activate RoomMaintenanceServiceImpl
deactivate RoomMaintenanceServiceImpl

RoomMaintenanceServiceImpl -> RoomMaintenanceRepository : save(new RoomMaintenance)
activate RoomMaintenanceRepository
RoomMaintenanceRepository --> RoomMaintenanceServiceImpl : return saved RoomMaintenance
deactivate RoomMaintenanceRepository

RoomMaintenanceServiceImpl -> RoomRepository : updateRoomStatus(roomId, "UNDER_MAINTENANCE")
activate RoomRepository
RoomRepository --> RoomMaintenanceServiceImpl : return updated Room
deactivate RoomRepository

RoomMaintenanceServiceImpl --> RoomMaintenanceController : return MaintenanceResponseDTO
deactivate RoomMaintenanceServiceImpl

RoomMaintenanceController --> ApiClient : HTTP 201 Created (JSON)
deactivate RoomMaintenanceController

ApiClient --> SetMaintenanceView : Promise resolved
deactivate ApiClient

SetMaintenanceView --> HKStaff : Display Success Toast ("Room locked for Maintenance")
deactivate SetMaintenanceView
@enduml
```

---

## 3. Mục 4.4: Reservation & Front-Desk Operations

### 3.1 UC-21 & UC-23 Search & Create Room Reservation
```plantuml
@startuml
skinparam shadowed false
autonumber 1 "0 : "

actor "Lifeline2: Customer" as Customer
participant BookingCheckoutView
participant ApiClient
participant ReservationController
participant ReservationServiceImpl
participant ReservationRepository
participant ReservationDetailRepository
participant MailNotificationService

Customer -> BookingCheckoutView : Fill guest info, dates & click "Confirm Booking"
activate BookingCheckoutView

BookingCheckoutView -> ApiClient : post("/api/v1/reservations", bookingDTO)
activate ApiClient

ApiClient -> ReservationController : createReservation(bookingDTO)
activate ReservationController

ReservationController -> ReservationServiceImpl : processBooking(bookingDTO)
activate ReservationServiceImpl

ReservationServiceImpl -> ReservationServiceImpl : checkAvailabilityQuota(dates, roomTypeId)
activate ReservationServiceImpl
deactivate ReservationServiceImpl

ReservationServiceImpl -> ReservationRepository : save(new Reservation)
activate ReservationRepository
ReservationRepository --> ReservationServiceImpl : return saved Reservation
deactivate ReservationRepository

ReservationServiceImpl -> ReservationDetailRepository : save(new ReservationDetail)
activate ReservationDetailRepository
ReservationDetailRepository --> ReservationServiceImpl : return saved Detail
deactivate ReservationDetailRepository

ReservationServiceImpl -> MailNotificationService : sendBookingConfirmationEmail(booking)
activate MailNotificationService
MailNotificationService --> ReservationServiceImpl : email dispatched
deactivate MailNotificationService

ReservationServiceImpl --> ReservationController : return ReservationResponseDTO
deactivate ReservationServiceImpl

ReservationController --> ApiClient : HTTP 201 Created (Booking Reference Code)
deactivate ReservationController

ApiClient --> BookingCheckoutView : Promise resolved
deactivate ApiClient

BookingCheckoutView --> Customer : Display Booking Confirmation ("Booking #HMS-9021 confirmed")
deactivate BookingCheckoutView
@enduml
```

### 3.2 UC-27 Check-in Guest
```plantuml
@startuml
skinparam shadowed false
autonumber 1 "0 : "

actor "Lifeline2: Front-Desk Staff" as Staff
participant CheckInView
participant ApiClient
participant JwtAuthenticationFilter
participant FrontDeskController
participant FrontDeskServiceImpl
participant ReservationRepository
participant RoomRepository
participant GuestStayRepository
participant StayRoomAssignmentRepository

Staff -> CheckInView : Input Booking Code & click "Check-in Guest"
activate CheckInView

CheckInView -> ApiClient : post("/api/v1/frontdesk/check-in", checkInDTO)
activate ApiClient

ApiClient -> JwtAuthenticationFilter : HTTP POST with Bearer Token
activate JwtAuthenticationFilter

JwtAuthenticationFilter -> FrontDeskController : checkInGuest(checkInDTO)
deactivate JwtAuthenticationFilter
activate FrontDeskController

FrontDeskController -> FrontDeskServiceImpl : performCheckIn(checkInDTO)
activate FrontDeskServiceImpl

FrontDeskServiceImpl -> ReservationRepository : findByCode(bookingCode)
activate ReservationRepository
ReservationRepository --> FrontDeskServiceImpl : return Reservation entity
deactivate ReservationRepository

FrontDeskServiceImpl -> RoomRepository : findAvailableCleanRoom(roomTypeId)
activate RoomRepository
RoomRepository --> FrontDeskServiceImpl : return assigned Room
deactivate RoomRepository

FrontDeskServiceImpl -> GuestStayRepository : save(new GuestStay)
activate GuestStayRepository
GuestStayRepository --> FrontDeskServiceImpl : return persisted GuestStay
deactivate GuestStayRepository

FrontDeskServiceImpl -> StayRoomAssignmentRepository : save(new Assignment)
activate StayRoomAssignmentRepository
StayRoomAssignmentRepository --> FrontDeskServiceImpl : return persisted Assignment
deactivate StayRoomAssignmentRepository

FrontDeskServiceImpl -> RoomRepository : updateRoomStatus(roomId, "OCCUPIED")
activate RoomRepository
RoomRepository --> FrontDeskServiceImpl : status updated
deactivate RoomRepository

FrontDeskServiceImpl --> FrontDeskController : return CheckInResponseDTO
deactivate FrontDeskServiceImpl

FrontDeskController --> ApiClient : HTTP 200 OK (Room Key & Stay Details)
deactivate FrontDeskController

ApiClient --> CheckInView : Promise resolved
deactivate ApiClient

CheckInView --> Staff : Display Check-in Success & Print Key Card
deactivate CheckInView
@enduml
```

---

## 4. Mục 4.5: UC-37 & UC-39 Check-out & Payment Settlement

```plantuml
@startuml
skinparam shadowed false
autonumber 1 "0 : "

actor "Lifeline2: Cashier / Front-Desk" as Cashier
participant BillingView
participant ApiClient
participant JwtAuthenticationFilter
participant BillingController
participant BillingServiceImpl
participant FolioRepository
participant InvoiceRepository
participant PaymentRepository
participant PaymentGateway

Cashier -> BillingView : Click "Settle Payment & Check-out" (stayId, method)
activate BillingView

BillingView -> ApiClient : post("/api/v1/billing/checkout", settlementDTO)
activate ApiClient

ApiClient -> JwtAuthenticationFilter : HTTP POST with Bearer Token
activate JwtAuthenticationFilter

JwtAuthenticationFilter -> BillingController : processCheckOutPayment(settlementDTO)
deactivate JwtAuthenticationFilter
activate BillingController

BillingController -> BillingServiceImpl : settleFolioAndCheckout(settlementDTO)
activate BillingServiceImpl

BillingServiceImpl -> FolioRepository : findByStayId(stayId)
activate FolioRepository
FolioRepository --> BillingServiceImpl : return Folio with AdditionalCharges & ServiceOrders
deactivate FolioRepository

BillingServiceImpl -> BillingServiceImpl : calculateGrandTotal(roomCharges, services, taxes)
activate BillingServiceImpl
deactivate BillingServiceImpl

BillingServiceImpl -> PaymentGateway : processElectronicCharge(amount, paymentDetails)
activate PaymentGateway
PaymentGateway --> BillingServiceImpl : charge authorized (transactionId)
deactivate PaymentGateway

BillingServiceImpl -> InvoiceRepository : save(new Invoice)
activate InvoiceRepository
InvoiceRepository --> BillingServiceImpl : return persisted Invoice
deactivate InvoiceRepository

BillingServiceImpl -> PaymentRepository : save(new Payment)
activate PaymentRepository
PaymentRepository --> BillingServiceImpl : return persisted Payment
deactivate PaymentRepository

BillingServiceImpl -> FolioRepository : closeFolio(folioId)
activate FolioRepository
FolioRepository --> BillingServiceImpl : folio closed
deactivate FolioRepository

BillingServiceImpl --> BillingController : return InvoiceReceiptDTO
deactivate BillingServiceImpl

BillingController --> ApiClient : HTTP 200 OK (Receipt Data)
deactivate BillingController

ApiClient --> BillingView : Promise resolved
deactivate ApiClient

BillingView --> Cashier : Display Receipt Modal & Trigger Print
deactivate BillingView
@enduml
```

---

## 5. Mục 4.6: UC-46 Generate Revenue Analytics Report

```plantuml
@startuml
skinparam shadowed false
autonumber 1 "0 : "

actor "Lifeline2: Hotel Manager" as Manager
participant ReportAnalyticsView
participant ApiClient
participant JwtAuthenticationFilter
participant ReportController
participant ReportServiceImpl
participant ReservationRepository
participant RoomRepository

Manager -> ReportAnalyticsView : Select Date Range (From - To) & click "Generate Revenue Report"
activate ReportAnalyticsView

ReportAnalyticsView -> ApiClient : get("/api/v1/reports/revenue?from=...&to=...")
activate ApiClient

ApiClient -> JwtAuthenticationFilter : HTTP GET with Bearer Token
activate JwtAuthenticationFilter

JwtAuthenticationFilter -> ReportController : getRevenueAnalytics(fromDate, toDate)
deactivate JwtAuthenticationFilter
activate ReportController

ReportController -> ReportServiceImpl : generateRevenueReport(fromDate, toDate)
activate ReportServiceImpl

ReportServiceImpl -> ReservationRepository : queryRevenueByPeriod(fromDate, toDate)
activate ReservationRepository
ReservationRepository --> ReportServiceImpl : return revenue aggregate dataset
deactivate ReservationRepository

ReportServiceImpl -> RoomRepository : queryOccupancyRates(fromDate, toDate)
activate RoomRepository
RoomRepository --> ReportServiceImpl : return occupancy dataset
deactivate RoomRepository

ReportServiceImpl -> ReportServiceImpl : compileSummaryKPIs(totalRev, adr, revPAR, occupancyPct)
activate ReportServiceImpl
deactivate ReportServiceImpl

ReportServiceImpl --> ReportController : return RevenueReportDTO
deactivate ReportServiceImpl

ReportController --> ApiClient : HTTP 200 OK (JSON Chart Data & Metrics)
deactivate ReportController

ApiClient --> ReportAnalyticsView : Promise resolved
deactivate ApiClient

ReportAnalyticsView -> ReportAnalyticsView : renderChartsAndKPICards()
activate ReportAnalyticsView
deactivate ReportAnalyticsView

ReportAnalyticsView --> Manager : Display Revenue Dashboard & Enable PDF Export
deactivate ReportAnalyticsView
@enduml
```
