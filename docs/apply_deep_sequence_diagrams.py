#!/usr/bin/env python3
"""
apply_deep_sequence_diagrams.py

Upgrades all 7 Sequence Diagrams for the Hotel Management System (HMS):
1. Removes COMET stereotypes (<<boundary>>, <<controller>>, etc.) for clean, uncluttered visual appeal.
2. Employs formal UML Object/Instance notation (:ClassName) on all lifelines.
3. Groups architectural tiers using styled boxes:
   - "Frontend Layer (Client Browser / React)" #F8FAFC
   - "Backend Layer (Spring Boot 3-Tier)" #F1F5F9
   - "Database Layer" #F8FAFC
4. Accurately reflects Spring Security filter chain:
   - UC-02 Login: /api/v1/auth/login is .permitAll() (permits request without JWT header).
   - Other UCs: Protected with Bearer JWT validation.
5. All 'alt' and 'group' guard conditions are written in ENGLISH with BOLD BLACK styling:
   - skinparam SequenceGroupFontColor #000000
   - skinparam SequenceGroupFontStyle bold
   - skinparam SequenceGroupHeaderFontColor #000000
   - skinparam SequenceGroupHeaderFontStyle bold
   - No manual square brackets to avoid blue hyperlink styling.
6. Multi-table write operations wrapped in 'group @Transactional: ACID Consistency'.
7. Renders all 7 diagrams via Kroki to PNG and updates both Markdown and Word documents.
"""

import os
import urllib.request
import docx
import xml.etree.ElementTree as ET

DOCX_PATH = "/Users/hieu/Desktop/sba/docs/HMS_SoftwareDesignTemplate-6.docx"
MD_PATH = "/Users/hieu/Desktop/sba/docs/Class + Sequence/Sequence Diagram(s) (PlantUML).md"
OUTPUT_DIR = "/Users/hieu/Desktop/sba/docs/Class + Sequence"

STYLE_HEADER = """skinparam shadowed false
autonumber 1 "0 : "
skinparam SequenceGroupFontColor #000000
skinparam SequenceGroupFontStyle bold
skinparam SequenceGroupHeaderFontColor #000000
skinparam SequenceGroupHeaderFontStyle bold
skinparam SequenceGroupBorderColor #334155
"""

SEQUENCE_DIAGRAMS = {
    "seq_42_login.png": {
        "title": "4.2: UC-02 User Login Flow",
        "docx_p_idx": 226,
        "puml": f"""@startuml
{STYLE_HEADER}
box "Frontend Layer (Client Browser / React)" #F8FAFC
    actor "Staff" as User
    participant ":LoginPage" as LoginPage
    participant ":ApiClient" as ApiClient
end box

box "Backend Layer (Spring Boot)" #F1F5F9
    participant ":JwtAuthenticationFilter" as JwtFilter
    participant ":AuthenticationController" as AuthCtrl
    participant ":AuthenticationServiceImpl" as AuthSvc
    participant ":JwtTokenProvider" as TokenProv
    participant ":UserRepository" as UserRepo
end box

box "Database Layer" #F8FAFC
    database ":Database" as DB
end box

User -> LoginPage : Input username & password, click "Login"
activate LoginPage

LoginPage -> LoginPage : validateLoginForm()

LoginPage -> ApiClient : post("/api/v1/auth/login", loginDTO)
activate ApiClient

note over JwtFilter : Endpoint /auth/login is permitAll()\\n(Permits request without JWT header)
ApiClient -> JwtFilter : HTTP POST /api/v1/auth/login
activate JwtFilter
JwtFilter -> AuthCtrl : login(loginDTO)
deactivate JwtFilter
activate AuthCtrl

AuthCtrl -> AuthSvc : authenticate(loginDTO)
activate AuthSvc

AuthSvc -> UserRepo : findByEmail(email)
activate UserRepo
UserRepo -> DB : SELECT * FROM tbl_user WHERE email = ?
activate DB
DB --> UserRepo : User record
deactivate DB
UserRepo --> AuthSvc : return User entity
deactivate UserRepo

AuthSvc -> AuthSvc : verifyPasswordHash(raw, hashed)

alt Valid Credentials & Active Account
    AuthSvc -> TokenProv : generateToken(user)
    activate TokenProv
    TokenProv --> AuthSvc : return jwtAccessToken
    deactivate TokenProv

    AuthSvc --> AuthCtrl : return AuthResponseDTO(token, role)
    AuthCtrl --> ApiClient : HTTP 200 OK (JWT, UserProfile)
    ApiClient --> LoginPage : Promise resolved
    LoginPage -> LoginPage : storeTokenInMemory(token)
    LoginPage --> User : Redirect to Dashboard (by Role)
else Invalid Credentials or Locked Account
    AuthSvc --> AuthCtrl : throw BadCredentialsException
    deactivate AuthSvc
    AuthCtrl --> ApiClient : HTTP 401 Unauthorized ("Invalid credentials")
    deactivate AuthCtrl
    ApiClient --> LoginPage : Promise rejected (401)
    deactivate ApiClient
    LoginPage --> User : Display Error ("Invalid email or password")
    deactivate LoginPage
end
@enduml"""
    },

    "seq_43_housekeeping.png": {
        "title": "4.3: UC-19 Update Housekeeping Status",
        "docx_p_idx": 258,
        "puml": f"""@startuml
{STYLE_HEADER}
box "Frontend Layer (Client Browser / React)" #F8FAFC
    actor "Housekeeping Staff" as HKStaff
    participant ":HousekeepingBoardView" as HKView
    participant ":ApiClient" as ApiClient
end box

box "Backend Layer (Spring Boot)" #F1F5F9
    participant ":JwtAuthenticationFilter" as JwtFilter
    participant ":HousekeepingController" as HKCtrl
    participant ":HousekeepingServiceImpl" as HKSvc
    participant ":RoomRepository" as RoomRepo
end box

box "Database Layer" #F8FAFC
    database ":Database" as DB
end box

HKStaff -> HKView : Click "Mark Clean" (roomId, remarks)
activate HKView

HKView -> ApiClient : put("/api/v1/housekeeping/rooms/{{id}}/cleanliness", dto)
activate ApiClient

ApiClient -> JwtFilter : HTTP PUT with Bearer Token
activate JwtFilter
JwtFilter -> JwtFilter : validateJwtToken()
JwtFilter -> HKCtrl : updateCleanliness(roomId, dto)
deactivate JwtFilter
activate HKCtrl

HKCtrl -> HKSvc : changeRoomCleanliness(roomId, dto)
activate HKSvc

HKSvc -> RoomRepo : findById(roomId)
activate RoomRepo
RoomRepo -> DB : SELECT * FROM tbl_room WHERE room_id = ?
activate DB
DB --> RoomRepo : Room record
deactivate DB
RoomRepo --> HKSvc : return Room entity
deactivate RoomRepo

alt Room Found & Eligible for Transition
    HKSvc -> RoomRepo : save(updatedRoom)
    activate RoomRepo
    RoomRepo -> DB : UPDATE tbl_room SET status = 'CLEAN'
    activate DB
    DB --> RoomRepo : 1 row updated
    deactivate DB
    RoomRepo --> HKSvc : return persisted Room
    deactivate RoomRepo

    HKSvc --> HKCtrl : return RoomStatusResponseDTO
    HKCtrl --> ApiClient : HTTP 200 OK (JSON)
    ApiClient --> HKView : Promise resolved
    HKView --> HKStaff : Display Success Toast ("Room marked as Clean")
else Room Not Found or Invalid State
    HKSvc --> HKCtrl : throw ResourceNotFoundException("Room not found")
    deactivate HKSvc
    HKCtrl --> ApiClient : HTTP 404 Not Found / 400 Bad Request
    deactivate HKCtrl
    ApiClient --> HKView : Promise rejected
    deactivate ApiClient
    HKView --> HKStaff : Display Error Toast ("Failed to update status")
    deactivate HKView
end
@enduml"""
    },

    "seq_43_maintenance.png": {
        "title": "4.3: UC-20 Set Room Maintenance",
        "docx_p_idx": 262,
        "puml": f"""@startuml
{STYLE_HEADER}
box "Frontend Layer (Client Browser / React)" #F8FAFC
    actor "Housekeeping Staff" as HKStaff
    participant ":SetMaintenanceView" as MaintView
    participant ":ApiClient" as ApiClient
end box

box "Backend Layer (Spring Boot)" #F1F5F9
    participant ":JwtAuthenticationFilter" as JwtFilter
    participant ":RoomMaintenanceController" as MaintCtrl
    participant ":RoomMaintenanceServiceImpl" as MaintSvc
    participant ":RoomRepository" as RoomRepo
    participant ":RoomMaintenanceRepository" as MaintRepo
end box

box "Database Layer" #F8FAFC
    database ":Database" as DB
end box

HKStaff -> MaintView : Submit Maintenance Form (roomId, defect, date)
activate MaintView

MaintView -> ApiClient : post("/api/v1/maintenance/rooms/{{id}}", dto)
activate ApiClient

ApiClient -> JwtFilter : HTTP POST with Bearer Token
activate JwtFilter
JwtFilter -> MaintCtrl : createMaintenance(roomId, dto)
deactivate JwtFilter
activate MaintCtrl

MaintCtrl -> MaintSvc : scheduleMaintenance(roomId, dto)
activate MaintSvc

MaintSvc -> RoomRepo : findById(roomId)
activate RoomRepo
RoomRepo -> DB : SELECT * FROM tbl_room WHERE room_id = ?
activate DB
DB --> RoomRepo : Room record
deactivate DB
RoomRepo --> MaintSvc : return Room entity
deactivate RoomRepo

MaintSvc -> MaintSvc : checkOccupancyStatus(room)

alt Room is Vacant (No Active Stay)
    group @Transactional: ACID Consistency
        MaintSvc -> MaintRepo : save(new RoomMaintenance)
        activate MaintRepo
        MaintRepo -> DB : INSERT INTO tbl_room_maintenance ...
        activate DB
        DB --> MaintRepo : 1 row inserted
        deactivate DB
        MaintRepo --> MaintSvc : return saved RoomMaintenance
        deactivate MaintRepo

        MaintSvc -> RoomRepo : updateRoomStatus(roomId, "UNDER_MAINTENANCE")
        activate RoomRepo
        RoomRepo -> DB : UPDATE tbl_room SET status = 'UNDER_MAINTENANCE'
        activate DB
        DB --> RoomRepo : 1 row updated
        deactivate DB
        RoomRepo --> MaintSvc : return updated Room
        deactivate RoomRepo
    end

    MaintSvc --> MaintCtrl : return MaintenanceResponseDTO
    MaintCtrl --> ApiClient : HTTP 201 Created (JSON)
    ApiClient --> MaintView : Promise resolved
    MaintView --> HKStaff : Display Success Toast ("Room locked for Maintenance")
else Room is Currently Occupied
    MaintSvc --> MaintCtrl : throw InvalidRoomStateException("Cannot maintain occupied room")
    deactivate MaintSvc
    MaintCtrl --> ApiClient : HTTP 400 Bad Request ("Room currently occupied")
    deactivate MaintCtrl
    ApiClient --> MaintView : Promise rejected (400)
    deactivate ApiClient
    MaintView --> HKStaff : Display Error ("Cannot set maintenance for occupied room")
    deactivate MaintView
end
@enduml"""
    },

    "seq_44_booking.png": {
        "title": "4.4: UC-23 Room Reservation",
        "docx_p_idx": 294,
        "puml": f"""@startuml
{STYLE_HEADER}
box "Frontend Layer (Client Browser / React)" #F8FAFC
    actor "Customer" as Customer
    participant ":BookingCheckoutView" as BookingView
    participant ":ApiClient" as ApiClient
end box

box "Backend Layer (Spring Boot)" #F1F5F9
    participant ":ReservationController" as ResCtrl
    participant ":ReservationServiceImpl" as ResSvc
    participant ":ReservationRepository" as ResRepo
    participant ":ReservationDetailRepository" as DetailRepo
    participant ":MailNotificationService" as MailSvc
end box

box "Database Layer" #F8FAFC
    database ":Database" as DB
end box

Customer -> BookingView : Fill guest info, dates & click "Confirm Booking"
activate BookingView

BookingView -> ApiClient : post("/api/v1/reservations", bookingDTO)
activate ApiClient

ApiClient -> ResCtrl : createReservation(bookingDTO)
activate ResCtrl

ResCtrl -> ResSvc : processBooking(bookingDTO)
activate ResSvc

ResSvc -> ResSvc : checkAvailabilityQuota(dates, roomTypeId)

alt Room Quota Available for Interval
    group @Transactional: ACID Consistency
        ResSvc -> ResRepo : save(new Reservation)
        activate ResRepo
        ResRepo -> DB : INSERT INTO tbl_reservation ...
        activate DB
        DB --> ResRepo : Reservation persisted
        deactivate DB
        ResRepo --> ResSvc : return saved Reservation
        deactivate ResRepo

        ResSvc -> DetailRepo : save(new ReservationDetail)
        activate DetailRepo
        DetailRepo -> DB : INSERT INTO tbl_reservation_detail ...
        activate DB
        DB --> DetailRepo : Detail persisted
        deactivate DB
        DetailRepo --> ResSvc : return saved Detail
        deactivate DetailRepo
    end

    ResSvc -> MailSvc : sendBookingConfirmationEmail(booking)
    activate MailSvc
    MailSvc --> ResSvc : email dispatched
    deactivate MailSvc

    ResSvc --> ResCtrl : return ReservationResponseDTO
    ResCtrl --> ApiClient : HTTP 201 Created (Booking Reference Code)
    ApiClient --> BookingView : Promise resolved
    BookingView --> Customer : Display Booking Confirmation ("Booking #HMS-9021 confirmed")
else Room Category Fully Booked
    ResSvc --> ResCtrl : throw RoomQuotaExceededException("No rooms available")
    deactivate ResSvc
    ResCtrl --> ApiClient : HTTP 409 Conflict ("Room category fully booked")
    deactivate ResCtrl
    ApiClient --> BookingView : Promise rejected (409)
    deactivate ApiClient
    BookingView --> Customer : Display Error ("Category fully booked, please select other dates")
    deactivate BookingView
end
@enduml"""
    },

    "seq_44_checkin.png": {
        "title": "4.4: UC-27 Guest Check-in",
        "docx_p_idx": 298,
        "puml": f"""@startuml
{STYLE_HEADER}
box "Frontend Layer (Client Browser / React)" #F8FAFC
    actor "Front-Desk Staff" as Staff
    participant ":CheckInView" as CheckInView
    participant ":ApiClient" as ApiClient
end box

box "Backend Layer (Spring Boot)" #F1F5F9
    participant ":JwtAuthenticationFilter" as JwtFilter
    participant ":FrontDeskController" as FDCtrl
    participant ":FrontDeskServiceImpl" as FDSvc
    participant ":ReservationRepository" as ResRepo
    participant ":RoomRepository" as RoomRepo
    participant ":GuestStayRepository" as StayRepo
    participant ":StayRoomAssignmentRepository" as AssignRepo
end box

box "Database Layer" #F8FAFC
    database ":Database" as DB
end box

Staff -> CheckInView : Input Booking Code & click "Check-in Guest"
activate CheckInView

CheckInView -> ApiClient : post("/api/v1/frontdesk/check-in", checkInDTO)
activate ApiClient

ApiClient -> JwtFilter : HTTP POST with Bearer Token
activate JwtFilter
JwtFilter -> FDCtrl : checkInGuest(checkInDTO)
deactivate JwtFilter
activate FDCtrl

FDCtrl -> FDSvc : performCheckIn(checkInDTO)
activate FDSvc

FDSvc -> ResRepo : findByCode(bookingCode)
activate ResRepo
ResRepo -> DB : SELECT * FROM tbl_reservation WHERE code = ?
activate DB
DB --> ResRepo : Reservation record
deactivate DB
ResRepo --> FDSvc : return Reservation entity
deactivate ResRepo

alt Valid Booking & Clean Room Available
    FDSvc -> RoomRepo : findAvailableCleanRoom(roomTypeId)
    activate RoomRepo
    RoomRepo -> DB : SELECT * FROM tbl_room WHERE status = 'CLEAN'
    activate DB
    DB --> RoomRepo : Clean Room
    deactivate DB
    RoomRepo --> FDSvc : return assigned Room
    deactivate RoomRepo

    group @Transactional: ACID Consistency (Persist Stay & Lock Room)
        FDSvc -> StayRepo : save(new GuestStay)
        activate StayRepo
        StayRepo -> DB : INSERT INTO tbl_guest_stay ...
        activate DB
        DB --> StayRepo : GuestStay persisted
        deactivate DB
        StayRepo --> FDSvc : return persisted GuestStay
        deactivate StayRepo

        FDSvc -> AssignRepo : save(new Assignment)
        activate AssignRepo
        AssignRepo -> DB : INSERT INTO tbl_stay_room_assignment ...
        activate DB
        DB --> AssignRepo : Assignment persisted
        deactivate DB
        AssignRepo --> FDSvc : return persisted Assignment
        deactivate AssignRepo

        FDSvc -> RoomRepo : updateRoomStatus(roomId, "OCCUPIED")
        activate RoomRepo
        RoomRepo -> DB : UPDATE tbl_room SET status = 'OCCUPIED'
        activate DB
        DB --> RoomRepo : status updated
        deactivate DB
        RoomRepo --> FDSvc : return updated Room
        deactivate RoomRepo
    end

    FDSvc --> FDCtrl : return CheckInResponseDTO
    FDCtrl --> ApiClient : HTTP 200 OK (Room Key & Stay Details)
    ApiClient --> CheckInView : Promise resolved
    CheckInView --> Staff : Display Check-in Success & Print RFID Key Card
else Booking Not Found or No Clean Room Ready
    FDSvc --> FDCtrl : throw BusinessException("No clean room available")
    deactivate FDSvc
    FDCtrl --> ApiClient : HTTP 400 Bad Request ("Invalid booking or no room ready")
    deactivate FDCtrl
    ApiClient --> CheckInView : Promise rejected (400)
    deactivate ApiClient
    CheckInView --> Staff : Display Error ("No clean room available for assignment")
    deactivate CheckInView
end
@enduml"""
    },

    "seq_45_billing.png": {
        "title": "4.5: UC-37 & UC-39 Check-out & Payment Settlement",
        "docx_p_idx": 326,
        "puml": f"""@startuml
{STYLE_HEADER}
box "Frontend Layer (Client Browser / React)" #F8FAFC
    actor "Cashier" as Cashier
    participant ":BillingView" as BillingView
    participant ":ApiClient" as ApiClient
end box

box "Backend Layer (Spring Boot)" #F1F5F9
    participant ":JwtAuthenticationFilter" as JwtFilter
    participant ":BillingController" as BillCtrl
    participant ":BillingServiceImpl" as BillSvc
    participant ":FolioRepository" as FolioRepo
    participant ":InvoiceRepository" as InvRepo
    participant ":PaymentRepository" as PayRepo
    participant ":PaymentGateway" as Gateway
end box

box "Database Layer" #F8FAFC
    database ":Database" as DB
end box

Cashier -> BillingView : Click "Settle Payment & Check-out" (stayId, method)
activate BillingView

BillingView -> ApiClient : post("/api/v1/billing/checkout", settlementDTO)
activate ApiClient

ApiClient -> JwtFilter : HTTP POST with Bearer Token
activate JwtFilter
JwtFilter -> BillCtrl : processCheckOutPayment(settlementDTO)
deactivate JwtFilter
activate BillCtrl

BillCtrl -> BillSvc : settleFolioAndCheckout(settlementDTO)
activate BillSvc

BillSvc -> FolioRepo : findByStayId(stayId)
activate FolioRepo
FolioRepo -> DB : SELECT * FROM tbl_folio WHERE stay_id = ?
activate DB
DB --> FolioRepo : Folio with orders & charges
deactivate DB
FolioRepo --> BillSvc : return Folio entity
deactivate FolioRepo

BillSvc -> BillSvc : calculateGrandTotal(charges, services, taxes)

BillSvc -> Gateway : processElectronicCharge(amount, paymentDetails)
activate Gateway

alt Payment Authorized & Card Approved
    Gateway --> BillSvc : charge authorized (transactionId)
    deactivate Gateway

    group @Transactional: ACID Consistency (Generate Invoice & Close Folio)
        BillSvc -> InvRepo : save(new Invoice)
        activate InvRepo
        InvRepo -> DB : INSERT INTO tbl_invoice ...
        activate DB
        DB --> InvRepo : Invoice persisted
        deactivate DB
        InvRepo --> BillSvc : return persisted Invoice
        deactivate InvRepo

        BillSvc -> PayRepo : save(new Payment)
        activate PayRepo
        PayRepo -> DB : INSERT INTO tbl_payment ...
        activate DB
        DB --> PayRepo : Payment persisted
        deactivate DB
        PayRepo --> BillSvc : return persisted Payment
        deactivate PayRepo

        BillSvc -> FolioRepo : closeFolio(folioId)
        activate FolioRepo
        FolioRepo -> DB : UPDATE tbl_folio SET status = 'CLOSED'
        activate DB
        DB --> FolioRepo : Folio closed
        deactivate DB
        FolioRepo --> BillSvc : status updated
        deactivate FolioRepo
    end

    BillSvc --> BillCtrl : return InvoiceReceiptDTO
    BillCtrl --> ApiClient : HTTP 200 OK (Receipt Data)
    ApiClient --> BillingView : Promise resolved
    BillingView --> Cashier : Display Receipt Modal & Trigger Print
else Payment Declined or Insufficient Funds
    Gateway --> BillSvc : charge declined (Error: Insufficient funds)
    activate Gateway
    deactivate Gateway
    BillSvc --> BillCtrl : throw PaymentDeclinedException("Card declined")
    deactivate BillSvc
    BillCtrl --> ApiClient : HTTP 400 Bad Request ("Payment failed")
    deactivate BillCtrl
    ApiClient --> BillingView : Promise rejected (400)
    deactivate ApiClient
    BillingView --> Cashier : Display Error ("Payment declined, request alternative method")
    deactivate BillingView
end
@enduml"""
    },

    "seq_46_report.png": {
        "title": "4.6: UC-46 Generate Revenue Analytics Report",
        "docx_p_idx": 354,
        "puml": f"""@startuml
{STYLE_HEADER}
box "Frontend Layer (Client Browser / React)" #F8FAFC
    actor "Hotel Manager" as Manager
    participant ":ReportAnalyticsView" as ReportView
    participant ":ApiClient" as ApiClient
end box

box "Backend Layer (Spring Boot)" #F1F5F9
    participant ":JwtAuthenticationFilter" as JwtFilter
    participant ":ReportController" as ReportCtrl
    participant ":ReportServiceImpl" as ReportSvc
    participant ":ReservationRepository" as ResRepo
    participant ":RoomRepository" as RoomRepo
end box

box "Database Layer" #F8FAFC
    database ":Database" as DB
end box

Manager -> ReportView : Select Date Range & click "Generate Revenue Report"
activate ReportView

ReportView -> ApiClient : get("/api/v1/reports/revenue?from=...&to=...")
activate ApiClient

ApiClient -> JwtFilter : HTTP GET with Bearer Token
activate JwtFilter
JwtFilter -> ReportCtrl : getRevenueAnalytics(fromDate, toDate)
deactivate JwtFilter
activate ReportCtrl

ReportCtrl -> ReportSvc : generateRevenueReport(fromDate, toDate)
activate ReportSvc

alt Valid Date Interval (From Date <= To Date)
    ReportSvc -> ResRepo : queryRevenueByPeriod(fromDate, toDate)
    activate ResRepo
    ResRepo -> DB : SELECT SUM(amount) FROM tbl_invoice WHERE date BETWEEN ? AND ?
    activate DB
    DB --> ResRepo : Aggregate revenue data
    deactivate DB
    ResRepo --> ReportSvc : return revenue dataset
    deactivate ResRepo

    ReportSvc -> RoomRepo : queryOccupancyRates(fromDate, toDate)
    activate RoomRepo
    RoomRepo -> DB : SELECT COUNT(*) FROM tbl_guest_stay ...
    activate DB
    DB --> RoomRepo : Occupancy counts
    deactivate DB
    RoomRepo --> ReportSvc : return occupancy dataset
    deactivate RoomRepo

    ReportSvc -> ReportSvc : compileSummaryKPIs(totalRev, adr, revPAR, occupancyPct)

    ReportSvc --> ReportCtrl : return RevenueReportDTO
    ReportCtrl --> ApiClient : HTTP 200 OK (JSON Chart Data & Metrics)
    ApiClient --> ReportView : Promise resolved
    ReportView -> ReportView : renderChartsAndKPICards()
    ReportView --> Manager : Display Revenue Dashboard & Enable PDF Export
else Invalid Date Range (From Date > To Date)
    ReportSvc --> ReportCtrl : throw InvalidDateRangeException("From date must be before To date")
    deactivate ReportSvc
    ReportCtrl --> ApiClient : HTTP 400 Bad Request ("Invalid date parameters")
    deactivate ReportCtrl
    ApiClient --> ReportView : Promise rejected (400)
    deactivate ApiClient
    ReportView --> Manager : Display Error ("From Date must be prior to To Date")
    deactivate ReportView
end
@enduml"""
    }
}

def render_plantuml_kroki(puml_text):
    req = urllib.request.Request(
        "https://kroki.io/plantuml/png",
        data=puml_text.encode("utf-8"),
        headers={
            "Content-Type": "text/plain; charset=utf-8",
            "User-Agent": "Mozilla/5.0"
        }
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read()

def main():
    print("=== Step 1: Rendering All 7 Professional Sequence Diagrams ===")
    rendered_images = {}
    for filename, diag_info in SEQUENCE_DIAGRAMS.items():
        print(f"Rendering {filename} ({diag_info['title']})...")
        png_bytes = render_plantuml_kroki(diag_info["puml"])
        out_path = os.path.join(OUTPUT_DIR, filename)
        with open(out_path, "wb") as f:
            f.write(png_bytes)
        rendered_images[filename] = png_bytes
        print(f"  -> Saved {out_path} ({len(png_bytes)} bytes)")

    print("\n=== Step 2: Updating Sequence Diagram(s) (PlantUML).md ===")
    md_sections = [
        "# Sequence Diagram(s) (PlantUML)\n",
        "Tài liệu thiết kế Sơ đồ tương tác đối tượng (Sequence Diagrams) cho các Use Case cốt lõi thuộc 5 phân hệ của hệ thống HMS.",
        "Thiết kế chuẩn kỹ nghệ phần mềm chuyên nghiệp: Phân tầng kiến trúc rõ ràng bằng các `box` (Frontend, Backend, Database), sử dụng đúng quy chuẩn Object (`:ClassName`), các điều kiện `alt` và `@Transactional` được viết bằng tiếng Anh với font chữ đậm màu đen, phản ánh chính xác cấu hình Spring Security (.permitAll vs Bearer Token) và đảm bảo tính toàn vẹn dữ liệu đa bảng.\n",
        "---\n"
    ]

    section_headings = {
        "seq_42_login.png": "## 1. Mục 4.2: UC-02 User Login Flow\n",
        "seq_43_housekeeping.png": "## 2. Mục 4.3: Room & Facility Management\n\n### 2.1 UC-19 Update Housekeeping Status\n",
        "seq_43_maintenance.png": "### 2.2 UC-20 Set Room Maintenance\n",
        "seq_44_booking.png": "## 3. Mục 4.4: Reservation & Front-Desk Operations\n\n### 3.1 UC-23 Room Reservation\n",
        "seq_44_checkin.png": "### 3.2 UC-27 Guest Check-in\n",
        "seq_45_billing.png": "## 4. Mục 4.5: UC-37 & UC-39 Check-out & Payment Settlement\n",
        "seq_46_report.png": "## 5. Mục 4.6: UC-46 Generate Revenue Analytics Report\n"
    }

    for filename, diag_info in SEQUENCE_DIAGRAMS.items():
        md_sections.append(section_headings[filename])
        md_sections.append("```plantuml\n" + diag_info["puml"] + "\n```\n\n---\n")

    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(md_sections))
    print(f"Updated {MD_PATH}")

    print("\n=== Step 3: Updating Word Document (HMS_SoftwareDesignTemplate-6.docx) ===")
    doc = docx.Document(DOCX_PATH)

    for filename, diag_info in SEQUENCE_DIAGRAMS.items():
        p_idx = diag_info["docx_p_idx"]
        p = doc.paragraphs[p_idx]
        found_embed = False
        for r in p.runs:
            if "blip" in r._r.xml:
                tree = ET.fromstring(r._r.xml)
                for elem in tree.iter():
                    if elem.tag.endswith("blip"):
                        embed_id = elem.attrib.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed")
                        part = doc.part.related_parts[embed_id]
                        part._blob = rendered_images[filename]
                        print(f"  -> Replaced image at P{p_idx} ({part.partname}) with {filename} ({len(rendered_images[filename])} bytes)")
                        found_embed = True
                        break
                if found_embed:
                    break

    doc.save(DOCX_PATH)
    print(f"Saved cleanly: {DOCX_PATH}")

if __name__ == "__main__":
    main()
