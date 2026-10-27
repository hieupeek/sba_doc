#!/usr/bin/env python3
"""
update_sequence_diagrams_vp_style.py

Refactors all 7 Sequence Diagrams in the Hotel Management System (HMS):
1. Distinguishes architectural tiers using Visual Paradigm styled boxes:
   - "Frontend Layer (Client Browser / React)" #F8FAFC
   - "Backend Layer (Spring Boot 3-Tier)" #F1F5F9
   - "Database Layer" #F8FAFC
2. Replaces Class-level participants with proper UML Objects (:ClassName).
3. Adds standard UML stereotypes:
   - <<boundary>> for UI Views and API Clients
   - <<security>> for JWT Filters
   - <<controller>> for Spring REST Controllers
   - <<service>> for Business Service Implementations
   - <<repository>> for Spring Data JPA Repositories
   - <<database>> for Database
   - <<external>> / <<utility>> for external integrations
4. Removes "Lifeline2:" prefix from Actors and standardizes Actor names.
5. Renders all 7 diagrams to PNG via Kroki.
6. Updates 'docs/Class + Sequence/Sequence Diagram(s) (PlantUML).md'.
7. Replaces the 7 embedded image parts in 'HMS_SoftwareDesignTemplate-6.docx'.
"""

import os
import urllib.request
import docx
import xml.etree.ElementTree as ET

DOCX_PATH = "/Users/hieu/Desktop/sba/docs/HMS_SoftwareDesignTemplate-6.docx"
MD_PATH = "/Users/hieu/Desktop/sba/docs/Class + Sequence/Sequence Diagram(s) (PlantUML).md"
OUTPUT_DIR = "/Users/hieu/Desktop/sba/docs/Class + Sequence"

SEQUENCE_DIAGRAMS = {
    "seq_42_login.png": {
        "title": "4.2: UC-02 User Login Flow",
        "docx_p_idx": 226,
        "puml": """@startuml
skinparam shadowed false
autonumber 1 "0 : "

box "Frontend Layer (Client Browser / React)" #F8FAFC
    actor "Nhân viên" as User
    participant ":LoginPage" as LoginPage <<boundary>>
    participant ":ApiClient" as ApiClient <<boundary>>
end box

box "Backend Layer (Spring Boot)" #F1F5F9
    participant ":JwtAuthenticationFilter" as JwtFilter <<security>>
    participant ":AuthenticationController" as AuthCtrl <<controller>>
    participant ":AuthenticationServiceImpl" as AuthSvc <<service>>
    participant ":JwtTokenProvider" as TokenProv <<utility>>
    participant ":UserRepository" as UserRepo <<repository>>
end box

box "Database Layer" #F8FAFC
    database ":Database" as DB <<database>>
end box

User -> LoginPage : Input username & password, click "Login"
activate LoginPage

LoginPage -> LoginPage : validateLoginForm()
activate LoginPage
deactivate LoginPage

LoginPage -> ApiClient : post("/api/v1/auth/login", loginDTO)
activate ApiClient

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
activate AuthSvc
deactivate AuthSvc

AuthSvc -> TokenProv : generateToken(user)
activate TokenProv
TokenProv --> AuthSvc : return jwtAccessToken
deactivate TokenProv

AuthSvc --> AuthCtrl : return AuthResponseDTO(token, role)
deactivate AuthSvc

AuthCtrl --> ApiClient : HTTP 200 OK (JWT, UserProfile)
deactivate AuthCtrl

ApiClient --> LoginPage : Promise resolved
deactivate ApiClient

LoginPage -> LoginPage : storeTokenInMemory(token)
activate LoginPage
deactivate LoginPage

LoginPage --> User : Redirect to Dashboard (by Role)
deactivate LoginPage
@enduml"""
    },

    "seq_43_housekeeping.png": {
        "title": "4.3: UC-19 Update Housekeeping Status",
        "docx_p_idx": 258,
        "puml": """@startuml
skinparam shadowed false
autonumber 1 "0 : "

box "Frontend Layer (Client Browser / React)" #F8FAFC
    actor "Nhân viên Buồng phòng" as HKStaff
    participant ":HousekeepingBoardView" as HKView <<boundary>>
    participant ":ApiClient" as ApiClient <<boundary>>
end box

box "Backend Layer (Spring Boot)" #F1F5F9
    participant ":JwtAuthenticationFilter" as JwtFilter <<security>>
    participant ":HousekeepingController" as HKCtrl <<controller>>
    participant ":HousekeepingServiceImpl" as HKSvc <<service>>
    participant ":RoomRepository" as RoomRepo <<repository>>
end box

box "Database Layer" #F8FAFC
    database ":Database" as DB <<database>>
end box

HKStaff -> HKView : Click "Mark Clean" (roomId, remarks)
activate HKView

HKView -> ApiClient : put("/api/v1/housekeeping/rooms/{id}/cleanliness", dto)
activate ApiClient

ApiClient -> JwtFilter : HTTP PUT with Bearer Token
activate JwtFilter

JwtFilter -> JwtFilter : validateJwtToken()
activate JwtFilter
deactivate JwtFilter

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

HKSvc -> HKSvc : verifyTransitionEligibility()
activate HKSvc
deactivate HKSvc

HKSvc -> RoomRepo : save(updatedRoom)
activate RoomRepo
RoomRepo -> DB : UPDATE tbl_room SET status = 'CLEAN'
activate DB
DB --> RoomRepo : 1 row updated
deactivate DB
RoomRepo --> HKSvc : return persisted Room
deactivate RoomRepo

HKSvc --> HKCtrl : return RoomStatusResponseDTO
deactivate HKSvc

HKCtrl --> ApiClient : HTTP 200 OK (JSON)
deactivate HKCtrl

ApiClient --> HKView : Promise resolved
deactivate ApiClient

HKView --> HKStaff : Display Success Toast ("Room marked as Clean")
deactivate HKView
@enduml"""
    },

    "seq_43_maintenance.png": {
        "title": "4.3: UC-20 Set Room Maintenance",
        "docx_p_idx": 262,
        "puml": """@startuml
skinparam shadowed false
autonumber 1 "0 : "

box "Frontend Layer (Client Browser / React)" #F8FAFC
    actor "Nhân viên Buồng phòng" as HKStaff
    participant ":SetMaintenanceView" as MaintView <<boundary>>
    participant ":ApiClient" as ApiClient <<boundary>>
end box

box "Backend Layer (Spring Boot)" #F1F5F9
    participant ":JwtAuthenticationFilter" as JwtFilter <<security>>
    participant ":RoomMaintenanceController" as MaintCtrl <<controller>>
    participant ":RoomMaintenanceServiceImpl" as MaintSvc <<service>>
    participant ":RoomRepository" as RoomRepo <<repository>>
    participant ":RoomMaintenanceRepository" as MaintRepo <<repository>>
end box

box "Database Layer" #F8FAFC
    database ":Database" as DB <<database>>
end box

HKStaff -> MaintView : Submit Maintenance Form (roomId, defect, date)
activate MaintView

MaintView -> ApiClient : post("/api/v1/maintenance/rooms/{id}", dto)
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
RoomRepo --> HKSvc : return Room entity
deactivate RoomRepo

MaintSvc -> MaintSvc : checkOccupancyStatus(room)
activate MaintSvc
deactivate MaintSvc

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

MaintSvc --> MaintCtrl : return MaintenanceResponseDTO
deactivate MaintSvc

MaintCtrl --> ApiClient : HTTP 201 Created (JSON)
deactivate MaintCtrl

ApiClient --> MaintView : Promise resolved
deactivate ApiClient

MaintView --> HKStaff : Display Success Toast ("Room locked for Maintenance")
deactivate MaintView
@enduml"""
    },

    "seq_44_booking.png": {
        "title": "4.4: UC-23 Room Reservation",
        "docx_p_idx": 294,
        "puml": """@startuml
skinparam shadowed false
autonumber 1 "0 : "

box "Frontend Layer (Client Browser / React)" #F8FAFC
    actor "Khách hàng" as Customer
    participant ":BookingCheckoutView" as BookingView <<boundary>>
    participant ":ApiClient" as ApiClient <<boundary>>
end box

box "Backend Layer (Spring Boot)" #F1F5F9
    participant ":ReservationController" as ResCtrl <<controller>>
    participant ":ReservationServiceImpl" as ResSvc <<service>>
    participant ":ReservationRepository" as ResRepo <<repository>>
    participant ":ReservationDetailRepository" as DetailRepo <<repository>>
    participant ":MailNotificationService" as MailSvc <<service>>
end box

box "Database Layer" #F8FAFC
    database ":Database" as DB <<database>>
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
activate ResSvc
deactivate ResSvc

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

ResSvc -> MailSvc : sendBookingConfirmationEmail(booking)
activate MailSvc
MailSvc --> ResSvc : email dispatched
deactivate MailSvc

ResSvc --> ResCtrl : return ReservationResponseDTO
deactivate ResSvc

ResCtrl --> ApiClient : HTTP 201 Created (Booking Reference Code)
deactivate ResCtrl

ApiClient --> BookingView : Promise resolved
deactivate ApiClient

BookingView --> Customer : Display Booking Confirmation ("Booking #HMS-9021 confirmed")
deactivate BookingView
@enduml"""
    },

    "seq_44_checkin.png": {
        "title": "4.4: UC-27 Guest Check-in",
        "docx_p_idx": 298,
        "puml": """@startuml
skinparam shadowed false
autonumber 1 "0 : "

box "Frontend Layer (Client Browser / React)" #F8FAFC
    actor "Lễ tân" as Staff
    participant ":CheckInView" as CheckInView <<boundary>>
    participant ":ApiClient" as ApiClient <<boundary>>
end box

box "Backend Layer (Spring Boot)" #F1F5F9
    participant ":JwtAuthenticationFilter" as JwtFilter <<security>>
    participant ":FrontDeskController" as FDCtrl <<controller>>
    participant ":FrontDeskServiceImpl" as FDSvc <<service>>
    participant ":ReservationRepository" as ResRepo <<repository>>
    participant ":RoomRepository" as RoomRepo <<repository>>
    participant ":GuestStayRepository" as StayRepo <<repository>>
    participant ":StayRoomAssignmentRepository" as AssignRepo <<repository>>
end box

box "Database Layer" #F8FAFC
    database ":Database" as DB <<database>>
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

FDSvc -> RoomRepo : findAvailableCleanRoom(roomTypeId)
activate RoomRepo
RoomRepo -> DB : SELECT * FROM tbl_room WHERE status = 'CLEAN'
activate DB
DB --> RoomRepo : Clean Room
deactivate DB
RoomRepo --> FDSvc : return assigned Room
deactivate RoomRepo

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

FDSvc --> FDCtrl : return CheckInResponseDTO
deactivate FDSvc

FDCtrl --> ApiClient : HTTP 200 OK (Room Key & Stay Details)
deactivate FDCtrl

ApiClient --> CheckInView : Promise resolved
deactivate ApiClient

CheckInView --> Staff : Display Check-in Success & Print Key Card
deactivate CheckInView
@enduml"""
    },

    "seq_45_billing.png": {
        "title": "4.5: UC-37 & UC-39 Check-out & Payment Settlement",
        "docx_p_idx": 326,
        "puml": """@startuml
skinparam shadowed false
autonumber 1 "0 : "

box "Frontend Layer (Client Browser / React)" #F8FAFC
    actor "Thu ngân" as Cashier
    participant ":BillingView" as BillingView <<boundary>>
    participant ":ApiClient" as ApiClient <<boundary>>
end box

box "Backend Layer (Spring Boot)" #F1F5F9
    participant ":JwtAuthenticationFilter" as JwtFilter <<security>>
    participant ":BillingController" as BillCtrl <<controller>>
    participant ":BillingServiceImpl" as BillSvc <<service>>
    participant ":FolioRepository" as FolioRepo <<repository>>
    participant ":InvoiceRepository" as InvRepo <<repository>>
    participant ":PaymentRepository" as PayRepo <<repository>>
    participant ":PaymentGateway" as Gateway <<external>>
end box

box "Database Layer" #F8FAFC
    database ":Database" as DB <<database>>
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
activate BillSvc
deactivate BillSvc

BillSvc -> Gateway : processElectronicCharge(amount, paymentDetails)
activate Gateway
Gateway --> BillSvc : charge authorized (transactionId)
deactivate Gateway

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

BillSvc --> BillCtrl : return InvoiceReceiptDTO
deactivate BillSvc

BillCtrl --> ApiClient : HTTP 200 OK (Receipt Data)
deactivate BillCtrl

ApiClient --> BillingView : Promise resolved
deactivate ApiClient

BillingView --> Cashier : Display Receipt Modal & Trigger Print
deactivate BillingView
@enduml"""
    },

    "seq_46_report.png": {
        "title": "4.6: UC-46 Generate Revenue Analytics Report",
        "docx_p_idx": 354,
        "puml": """@startuml
skinparam shadowed false
autonumber 1 "0 : "

box "Frontend Layer (Client Browser / React)" #F8FAFC
    actor "Ban Quản lý" as Manager
    participant ":ReportAnalyticsView" as ReportView <<boundary>>
    participant ":ApiClient" as ApiClient <<boundary>>
end box

box "Backend Layer (Spring Boot)" #F1F5F9
    participant ":JwtAuthenticationFilter" as JwtFilter <<security>>
    participant ":ReportController" as ReportCtrl <<controller>>
    participant ":ReportServiceImpl" as ReportSvc <<service>>
    participant ":ReservationRepository" as ResRepo <<repository>>
    participant ":RoomRepository" as RoomRepo <<repository>>
end box

box "Database Layer" #F8FAFC
    database ":Database" as DB <<database>>
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
activate ReportSvc
deactivate ReportSvc

ReportSvc --> ReportCtrl : return RevenueReportDTO
deactivate ReportSvc

ReportCtrl --> ApiClient : HTTP 200 OK (JSON Chart Data & Metrics)
deactivate ReportCtrl

ApiClient --> ReportView : Promise resolved
deactivate ApiClient

ReportView -> ReportView : renderChartsAndKPICards()
activate ReportView
deactivate ReportView

ReportView --> Manager : Display Revenue Dashboard & Enable PDF Export
deactivate ReportView
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
    print("=== Step 1: Rendering all 7 Visual Paradigm-styled Sequence Diagrams ===")
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
        "Thiết kế chuẩn Visual Paradigm: Phân tầng kiến trúc rõ ràng bằng các `box` (Frontend, Backend, Database), sử dụng đúng quy chuẩn Object (`:ClassName`), gán đầy đủ Stereotype (`<<boundary>>`, `<<controller>>`, `<<service>>`, `<<repository>>`, `<<database>>`), thể hiện chi tiết self-call, activation bar và mũi tên phản hồi.\n",
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
