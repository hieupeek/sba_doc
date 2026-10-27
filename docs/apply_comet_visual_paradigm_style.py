#!/usr/bin/env python3
"""
apply_comet_visual_paradigm_style.py

Refactors all 7 Sequence Diagrams in the Hotel Management System (HMS) to strictly match:
- COMET Method: <<boundary>> for UI pages, <<control>> for Controllers and Services, and Database.
- Exact Visual Paradigm Community Edition aesthetic from reference image.png:
  - Header background: Sky Blue #67C8FF
  - Activation bar background: Sky Blue #67C8FF
  - Dark borders #000000
  - 'hide footbox' (clean single top row of lifelines)
  - English 'alt' frames with bold black font: [Condition text]
- Clean message passing between objects from Actor -> Boundary -> Control -> Control -> Database.
"""

import os
import urllib.request
import docx
import xml.etree.ElementTree as ET

DOCX_PATH = "/Users/hieu/Desktop/sba/docs/HMS_SoftwareDesignTemplate-6.docx"
MD_PATH = "/Users/hieu/Desktop/sba/docs/Class + Sequence/Sequence Diagram(s) (PlantUML).md"
OUTPUT_DIR = "/Users/hieu/Desktop/sba/docs/Class + Sequence"

STYLE_HEADER = """skinparam shadowed false
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
"""

SEQUENCE_DIAGRAMS = {
    "seq_42_login.png": {
        "title": "4.2: UC-02 User Login Flow",
        "docx_p_idx": 226,
        "puml": f"""@startuml
{STYLE_HEADER}
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
@enduml"""
    },

    "seq_43_housekeeping.png": {
        "title": "4.3: UC-19 Update Housekeeping Status",
        "docx_p_idx": 258,
        "puml": f"""@startuml
{STYLE_HEADER}
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
@enduml"""
    },

    "seq_43_maintenance.png": {
        "title": "4.3: UC-20 Set Room Maintenance",
        "docx_p_idx": 262,
        "puml": f"""@startuml
{STYLE_HEADER}
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
@enduml"""
    },

    "seq_44_booking.png": {
        "title": "4.4: UC-23 Room Reservation",
        "docx_p_idx": 294,
        "puml": f"""@startuml
{STYLE_HEADER}
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
@enduml"""
    },

    "seq_44_checkin.png": {
        "title": "4.4: UC-27 Guest Check-in",
        "docx_p_idx": 298,
        "puml": f"""@startuml
{STYLE_HEADER}
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
@enduml"""
    },

    "seq_45_billing.png": {
        "title": "4.5: UC-37 & UC-39 Check-out & Payment Settlement",
        "docx_p_idx": 326,
        "puml": f"""@startuml
{STYLE_HEADER}
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
@enduml"""
    },

    "seq_46_report.png": {
        "title": "4.6: UC-46 Generate Revenue Analytics Report",
        "docx_p_idx": 354,
        "puml": f"""@startuml
{STYLE_HEADER}
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
    print("=== Step 1: Rendering All 7 COMET Visual Paradigm Sequence Diagrams ===")
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
        "Thiết kế chuẩn phương pháp COMET & Visual Paradigm: Áp dụng đầy đủ stereotype `<<boundary>>` cho các trang giao diện, `<<control>>` cho Controller và Service, và `Database` cho tầng CSDL. Sử dụng phong cách thẩm mỹ Visual Paradigm với màu xanh Cyan #67C8FF, các khung `alt` điều kiện tiếng Anh in đậm màu đen, thể hiện luồng trao đổi thông điệp hoàn chỉnh từ Actor -> Boundary -> Control -> Database.\n",
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
