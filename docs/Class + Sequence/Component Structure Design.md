# Backend Class/Component Structure Design (PlantUML)

Tài liệu thiết kế cấu trúc thành phần tầng Backend cho toàn bộ 5 phân hệ của hệ thống Hotel Management System (HMS).
Được thiết kế chuẩn theo 6 loại quan hệ UML trong SKILL.md và đồng nhất 100% với CSDL quan hệ trong Section 5:
- **Inheritance (`--|>`):** Kế thừa lớp cha / repository base.
- **Realization (`..|>`):** ServiceImpl hiện thực hóa Service interface.
- **Dependency (`..>`):** Controller sử dụng Service, Repository trả về Entity.
- **Association (`-->`):** Liên kết có hướng chuẩn mực (Service giữ tham chiếu điều hướng Repository thông qua Dependency Injection; Entity tham chiếu Entity khác thông qua khóa ngoại, ví dụ `User --> Role`, `Room --> Room_Type`, `Review --> Guest_Stay`, `Invoice --> Voucher`, `Payment --> Reservation`).
- **Composition (`*--`):** Has-a chặt chẽ phụ thuộc vòng đời (Reservation sở hữu Reservation_Detail, Guest_Stay sở hữu Stay_Room_Assignment, Folio sở hữu Additional_Charge, Payment sở hữu Payment_Attempt).
- **Aggregation (`o--`):** Has-a sở hữu lỏng lẻo toàn thể - bộ phận (Whole-Part độc lập).

---

## 1. Mục 4.2: Account & Authentication Management

```plantuml
@startuml
skinparam shadowed false
hide circle

' 1. Declaration of Classes
class UserController <<controller>>
class AuthenticationController <<controller>>
class JwtAuthenticationFilter <<security>>
class JwtTokenProvider

interface UserService <<interface>>
interface AuthenticationService <<interface>>

class UserServiceImpl <<service>>
class AuthenticationServiceImpl <<service>>

class UserRepository <<repository>>
class RoleRepository <<repository>>

class User <<entity>>
class Role <<entity>>

' 2. Realization (..|>)
UserServiceImpl ..|> UserService
AuthenticationServiceImpl ..|> AuthenticationService

' 3. Dependency (..>)
UserController ..> UserService
AuthenticationController ..> AuthenticationService
JwtAuthenticationFilter ..> JwtTokenProvider
JwtAuthenticationFilter ..> AuthenticationService
UserRepository ..> User
RoleRepository ..> Role

' 4. Association (-->)
UserServiceImpl --> UserRepository
AuthenticationServiceImpl --> UserRepository
AuthenticationServiceImpl --> RoleRepository
User --> Role

@enduml
```

---

## 2. Mục 4.3: Room & Facility Management (Housekeeping & Maintenance)

```plantuml
@startuml
skinparam shadowed false
hide circle

' 1. Declaration of Classes
class RoomController <<controller>>
class HousekeepingController <<controller>>
class RoomMaintenanceController <<controller>>

interface RoomService <<interface>>
interface HousekeepingService <<interface>>
interface RoomMaintenanceService <<interface>>

class RoomServiceImpl <<service>>
class HousekeepingServiceImpl <<service>>
class RoomMaintenanceServiceImpl <<service>>

class RoomRepository <<repository>>
class RoomTypeRepository <<repository>>
class RoomMaintenanceRepository <<repository>>

class Room <<entity>>
class Room_Type <<entity>>
class Room_Maintenance <<entity>>
class User <<entity>>

' 2. Realization (..|>)
RoomServiceImpl ..|> RoomService
HousekeepingServiceImpl ..|> HousekeepingService
RoomMaintenanceServiceImpl ..|> RoomMaintenanceService

' 3. Dependency (..>)
RoomController ..> RoomService
HousekeepingController ..> HousekeepingService
RoomMaintenanceController ..> RoomMaintenanceService
RoomRepository ..> Room
RoomTypeRepository ..> Room_Type
RoomMaintenanceRepository ..> Room_Maintenance

' 4. Association (-->)
RoomServiceImpl --> RoomRepository
RoomServiceImpl --> RoomTypeRepository
HousekeepingServiceImpl --> RoomRepository
RoomMaintenanceServiceImpl --> RoomMaintenanceRepository
RoomMaintenanceServiceImpl --> RoomRepository
Room --> Room_Type
Room_Maintenance --> Room
Room_Maintenance --> User

@enduml
```

---

## 3. Mục 4.4: Reservation & Front-Desk Operations

```plantuml
@startuml
skinparam shadowed false
hide circle

' 1. Declaration of Classes
class ReservationController <<controller>>
class FrontDeskController <<controller>>

interface ReservationService <<interface>>
interface FrontDeskService <<interface>>

class ReservationServiceImpl <<service>>
class FrontDeskServiceImpl <<service>>

class ReservationRepository <<repository>>
class ReservationDetailRepository <<repository>>
class GuestStayRepository <<repository>>
class StayRoomAssignmentRepository <<repository>>

class Reservation <<entity>>
class Reservation_Detail <<entity>>
class Guest_Stay <<entity>>
class Stay_Room_Assignment <<entity>>
class Customer <<entity>>
class Room <<entity>>
class Room_Type <<entity>>

' 2. Realization (..|>)
ReservationServiceImpl ..|> ReservationService
FrontDeskServiceImpl ..|> FrontDeskService

' 3. Dependency (..>)
ReservationController ..> ReservationService
FrontDeskController ..> FrontDeskService
ReservationRepository ..> Reservation
ReservationDetailRepository ..> Reservation_Detail
GuestStayRepository ..> Guest_Stay
StayRoomAssignmentRepository ..> Stay_Room_Assignment

' 4. Association (-->)
ReservationServiceImpl --> ReservationRepository
ReservationServiceImpl --> ReservationDetailRepository
FrontDeskServiceImpl --> GuestStayRepository
FrontDeskServiceImpl --> StayRoomAssignmentRepository
FrontDeskServiceImpl --> ReservationRepository
Reservation --> Customer
Guest_Stay --> Reservation
Reservation_Detail --> Room_Type
Stay_Room_Assignment --> Room

' 5. Composition (*--)
Reservation *-- Reservation_Detail
Guest_Stay *-- Stay_Room_Assignment

@enduml
```

---

## 4. Mục 4.5: Ancillary Services & Billing Management

```plantuml
@startuml
skinparam shadowed false
hide circle

' 1. Declaration of Classes
class HotelServiceController <<controller>>
class ServiceOrderController <<controller>>
class BillingController <<controller>>
class PaymentController <<controller>>

interface HotelServiceService <<interface>>
interface ServiceOrderService <<interface>>
interface BillingService <<interface>>
interface PaymentService <<interface>>

class HotelServiceServiceImpl <<service>>
class ServiceOrderServiceImpl <<service>>
class BillingServiceImpl <<service>>
class PaymentServiceImpl <<service>>

class HotelServiceRepository <<repository>>
class ServiceOrderRepository <<repository>>
class FolioRepository <<repository>>
class AdditionalChargeRepository <<repository>>
class InvoiceRepository <<repository>>
class PaymentRepository <<repository>>
class PaymentAttemptRepository <<repository>>
class VoucherRepository <<repository>>

class Hotel_Service <<entity>>
class Service_Order <<entity>>
class Folio <<entity>>
class Additional_Charge <<entity>>
class Invoice <<entity>>
class Payment <<entity>>
class Payment_Attempt <<entity>>
class Voucher <<entity>>
class Guest_Stay <<entity>>
class Reservation <<entity>>
class User <<entity>>

' 2. Realization (..|>)
HotelServiceServiceImpl ..|> HotelServiceService
ServiceOrderServiceImpl ..|> ServiceOrderService
BillingServiceImpl ..|> BillingService
PaymentServiceImpl ..|> PaymentService

' 3. Dependency (..>)
HotelServiceController ..> HotelServiceService
ServiceOrderController ..> ServiceOrderService
BillingController ..> BillingService
PaymentController ..> PaymentService
HotelServiceRepository ..> Hotel_Service
ServiceOrderRepository ..> Service_Order
FolioRepository ..> Folio
AdditionalChargeRepository ..> Additional_Charge
InvoiceRepository ..> Invoice
PaymentRepository ..> Payment
PaymentAttemptRepository ..> Payment_Attempt
VoucherRepository ..> Voucher

' 4. Association (-->)
HotelServiceServiceImpl --> HotelServiceRepository
ServiceOrderServiceImpl --> ServiceOrderRepository
ServiceOrderServiceImpl --> AdditionalChargeRepository
BillingServiceImpl --> FolioRepository
BillingServiceImpl --> AdditionalChargeRepository
BillingServiceImpl --> InvoiceRepository
BillingServiceImpl --> VoucherRepository
PaymentServiceImpl --> PaymentRepository
PaymentServiceImpl --> InvoiceRepository
PaymentServiceImpl --> PaymentAttemptRepository
Service_Order --> Hotel_Service
Service_Order --> Guest_Stay
Folio --> Guest_Stay
Additional_Charge --> User
Invoice --> Folio
Invoice --> Voucher
Payment --> Invoice
Payment --> Reservation

' 5. Composition (*--)
Folio *-- Additional_Charge
Payment *-- Payment_Attempt

@enduml
```

---

## 5. Mục 4.6: Reviews, Audit & Reporting Management

```plantuml
@startuml
skinparam shadowed false
hide circle

' 1. Declaration of Classes
class ReviewController <<controller>>
class ReportController <<controller>>

interface ReviewService <<interface>>
interface ReportService <<interface>>

class ReviewServiceImpl <<service>>
class ReportServiceImpl <<service>>

class ReviewRepository <<repository>>
class ReservationRepository <<repository>>
class RoomRepository <<repository>>

class Review <<entity>>
class Customer <<entity>>
class Guest_Stay <<entity>>
class Reservation <<entity>>
class Room <<entity>>

' 2. Realization (..|>)
ReviewServiceImpl ..|> ReviewService
ReportServiceImpl ..|> ReportService

' 3. Dependency (..>)
ReviewController ..> ReviewService
ReportController ..> ReportService
ReviewRepository ..> Review
ReservationRepository ..> Reservation
RoomRepository ..> Room
ReportServiceImpl ..> RoomRepository

' 4. Association (-->)
ReviewServiceImpl --> ReviewRepository
ReportServiceImpl --> ReservationRepository
ReportServiceImpl --> RoomRepository
Review --> Customer
Review --> Guest_Stay

@enduml
```
