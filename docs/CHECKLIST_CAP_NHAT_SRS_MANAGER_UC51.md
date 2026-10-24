# KẾ HOẠCH CẬP NHẬT TÀI LIỆU ĐẶC TẢ YÊU CẦU PHẦN MỀM (SRS)
## DỰ ÁN: HOTEL MANAGEMENT SYSTEM (HMS)
**Tài liệu áp dụng:** `HMS_SoftwareRequirementSpecification-4.docx`  
**Ngày lập:** 24/10/2026  
**Lý do cập nhật:** 
1. Tách vai trò `Administrator` thành 2 vai trò riêng biệt: **`Administrator`** (Quản trị viên kỹ thuật IT) và **`Manager`** (Quản lý nghiệp vụ khách sạn).
2. Bổ sung thêm **`UC-51: Assign Room Cleaning Task`** (Gán phòng dọn dẹp cho nhân viên buồng phòng).

---

## 📌 BẢNG TỔNG HỢP NHIỆM VỤ & PHÂN CÔNG (ACTION CHECKLIST)

| STT | Vị trí trong SRS | Hạng mục cần sửa | Chi tiết công việc cần làm | Phụ trách | Trạng thái |
|:---:|:---|:---|:---|:---:|:---:|
| **1** | **Bìa & Mục I** | Record of Changes (Table 0) | Thêm 1 dòng ghi nhận cập nhật phiên bản (v1.3/v2.0) | Nhóm trưởng | ⏳ Chưa làm |
| **2** | **Mục 1.2** | Context Diagram (Figure 1-1) | Kiểm tra và vẽ lại sơ đồ ngữ cảnh có thêm Actor `Manager` | Designer/Draw | ⏳ Chưa làm |
| **3** | **Mục 2.2** | Tổng số Use Case & Mô tả Subsystem | Sửa "50 use cases" thành "51 use cases", Subsystem 2 có 11 UCs | Thành viên A | ⏳ Chưa làm |
| **4** | **Mục 2.2.1** | Use Case Diagrams (Figures 2-1 -> 2-5) | Vẽ thêm Actor `Manager`, nối `UC-51`, đổi actor các UC quản lý sang Manager | Designer/Draw | ⏳ Chưa làm |
| **5** | **Mục 2.2.2** | Table 2 (Use Case Descriptions) | Đổi Actor từ `Administrator` sang `Manager` ở các UC quản lý; sửa `UC-09` thêm role Manager | Thành viên B | ⏳ Chưa làm |
| **6** | **Mục 3.1.3** | Table 4 (Screen Authorization) **[LỖI LỚN]** | Thêm cột `Manager`, thêm màn hình UC-51, phân bổ lại dấu `X` quyền hạn | Thành viên B | ⏳ Chưa làm |
| **7** | **Mục 3.6** | Chi tiết chức năng UC-51 | Viết mục **3.6.6 UC-51**: Mock-up, Screen Definition, Use Case Description, Alternative Flows | Thành viên C | ⏳ Chưa làm |
| **8** | **Mục 6.1** | Business Rules (Table 61) | Sửa **BR-06** thêm `Manager`, bổ sung **BR-43** cho UC-51 | Thành viên A | ⏳ Chưa làm |

---

## 🔍 CHI TIẾT CÁC ĐIỂM CẦN CHỈNH SỬA THEO TỪNG PHẦN

### 1. Mục I – Record of Changes (Bảng 0: Lịch sử phiên bản)
Thêm 1 dòng vào cuối bảng lịch sử thay đổi:
* **Date:** `24/10/2026` (hoặc ngày nộp).
* **A* M, D:** `M, A` (Modified & Added).
* **Author:** *(Tên thành viên sửa)*.
* **Description:** 
  > *"Tách vai trò Administrator thành Administrator (Quản trị hệ thống) và Manager (Quản lý nghiệp vụ); Bổ sung UC-51 Assign Room Cleaning Task vào Subsystem 2; Cập nhật ma trận phân quyền Table 4, sơ đồ Use Case Diagrams, Bảng Use Case Description và Business Rule BR-06."*

---

### 2. Mục 1.2 – Sơ đồ ngữ cảnh hệ thống (Figure 1-1: Context Diagram)
* **Hiện trạng:** Đoạn văn bản 53 & 54 đã mô tả `Manager` và `Administrator`, nhưng sơ đồ hình vẽ **Figure 1-1** cần kiểm tra lại.
* **Yêu cầu:** Sơ đồ Figure 1-1 bắt buộc phải có hộp/actor **`Manager`** kết nối với HMS, phân biệt rõ với **`Administrator`**.

---

### 3. Mục 2.2 – Phần giới thiệu Use Cases (Trang mở đầu mục 2.2)
* **Hiện trạng lỗi:**
  * Đoạn văn 69 ghi: *"The system provides 50 use cases partitioned into five functional subsystems:"*
  * Đoạn văn 71 ghi: *"Subsystem 2: Room & Facility Management (UC11 – UC20)"*
* **Sửa lại thành:**
  * *"The system provides **51 use cases** partitioned into five functional subsystems:"*
  * *"Subsystem 2: Room & Facility Management **(UC11 – UC20, UC-51)**: Covers room category configuration, inventory setup, room browsing, housekeeping workflow, **cleaning task assignment**, and maintenance tracking."* (Gồm **11 use cases**).

---

### 4. Mục 2.2.1 – Biểu đồ Use Case (Use Case Diagrams)
Cần cập nhật các hình vẽ biểu đồ Use Case của các phân hệ:
1. **Figure 2-1: Subsystem 1 (Account & Authentication):**
   * Actor `Administrator` chỉ nối tới các UC kỹ thuật: `UC-07 (Manage User Accounts)`, `UC-08 (Toggle Status)`, `UC-09 (Assign Roles)`.
2. **Figure 2-2: Subsystem 2 (Room & Facility Management):**
   * **Thêm Actor `Manager`** vào biểu đồ.
   * Nối `Manager` $\rightarrow$ **`UC-51: Assign Room Cleaning Task`**.
   * Chuyển các đường nối của nhóm quản lý phòng: `UC-11 (Create Room Type)`, `UC-12 (Update Room Type)`, `UC-13 (Deactivate Room Type)`, `UC-15 (Create Room)`, `UC-16 (Update Room)`, `UC-17 (Archive Room)` từ `Administrator` sang **`Manager`**.
3. **Figure 2-4: Subsystem 4 (Ancillary Services & Billing):**
   * Chuyển các UC quản lý giá & dịch vụ: `UC-31 (Create Service)`, `UC-32 (Update Tariff)`, `UC-33 (Deactivate Service)` sang Actor **`Manager`**.
4. **Figure 2-5: Subsystem 5 (Reviews, Audit & Reporting):**
   * Chuyển các UC nghiệp vụ: `UC-43 (Publish Reply)`, `UC-44 (Moderate Review)`, `UC-45 (Occupancy Report)`, `UC-46 (Revenue Analytics)`, `UC-47 (Service Analytics)`, `UC-50 (Export Dashboard)` sang Actor **`Manager`**.
   * `UC-48 (Configure Audit Parameters)` vẫn thuộc về **`Administrator`**.
   * `UC-49 (Inspect Audit Logs)`: Cả **`Administrator`** (Security Audit Logs) và **`Manager`** (Operational Audit Logs) đều có quyền xem.

---

### 5. Mục 2.2.2 – Bảng tổng hợp Use Case (Table 2: Use Case Descriptions)
Trong Bảng 2, cần rà soát và đổi giá trị cột **`Actor`** ở các dòng sau:

| Mã UC | Tên Use Case | Actor CŨ (Sai) | Actor MỚI (Đúng chuẩn) |
|:---:|:---|:---:|:---:|
| **UC-11** | Create Room Type | `Administrator` | **`Manager`** |
| **UC-12** | Update Room Type Details | `Administrator` | **`Manager`** |
| **UC-13** | Deactivate Room Category | `Administrator` | **`Manager`** |
| **UC-14** | View Room Categories | `Customer, Front-Desk Staff, Administrator` | `Customer, Front-Desk Staff, Manager` |
| **UC-15** | Create Room | `Administrator` | **`Manager`** |
| **UC-16** | Update Room Details | `Administrator` | **`Manager`** |
| **UC-17** | Archive Room | `Administrator` | **`Manager`** |
| **UC-18** | View Room Inventory | `Front-Desk Staff, Housekeeping Staff, Administrator` | `Front-Desk Staff, Housekeeping Staff, Manager` |
| **UC-20** | Set Room Maintenance | `Housekeeping Staff, Administrator` | `Housekeeping Staff, Manager` |
| **UC-31** | Create Hotel Service | `Administrator` | **`Manager`** |
| **UC-32** | Update Service Tariff | `Administrator` | **`Manager`** |
| **UC-33** | Deactivate Hotel Service | `Administrator` | **`Manager`** |
| **UC-43** | Publish Management Reply | `Front-Desk Staff, Administrator` | `Front-Desk Staff, Manager` |
| **UC-44** | Moderate Review Visibility | `Administrator` | **`Manager`** |
| **UC-45** | Generate Room Occupancy Report | `Administrator` | **`Manager`** |
| **UC-46** | Generate Revenue Analytics Report | `Administrator` | **`Manager`** |
| **UC-47** | Analyze Service Consumption | `Administrator` | **`Manager`** |
| **UC-49** | Inspect System Audit Logs | `Administrator` | **`Manager, Administrator`** |
| **UC-50** | Export Management Dashboard Summary | `Administrator` | **`Manager`** |
| **UC-51** | Assign Room Cleaning Task | *(Đã có)* | **`Manager`** *(Kiểm tra nội dung chuẩn)* |

> ⚠️ **ĐẶC BIỆT LƯU Ý TẠI UC-09 (Assign User Roles):**
> Trong dòng mô tả Main flow của `UC-09`, bước 2 hiện tại ghi:
> *"Administrator selects new role (Front-Desk Staff, Housekeeping Staff, Service Staff, Administrator)."*  
> 👉 **Bắt buộc phải sửa thành:**  
> *"Administrator selects new role (Front-Desk Staff, Housekeeping Staff, Service Staff, **Manager**, Administrator)."*

---

### 6. Mục 3.1.3 – Ma trận phân quyền màn hình (Table 4: Screen Authorization)
Đây là phần **bị thiếu sót nặng nhất** trong bản SRS-4 hiện tại vì bảng vẫn chỉ có 8 cột và chưa hề có cột `Manager`.

#### Hướng dẫn sửa Bảng 4:
1. **Chèn thêm 1 cột mới mang tên `Manager`** (đặt cạnh cột `Administrator`). Bảng nâng lên thành 9 cột:
   `[#, Screen / Function, Guest / Public, Customer, Front-Desk Staff, Housekeeping Staff, Service Staff, Manager, Administrator]`
2. **Thêm dòng màn hình cho UC-51:**
   * Tên màn hình: **`Assign Cleaning Tasks`** (Gán việc dọn phòng).
   * Đánh dấu `X` ở cột **`Manager`**.
3. **Phân bổ lại các dấu `X` quyền truy cập:**
   * **Cột `Manager` (Đánh dấu `X` tại):**
     * User Profile, Update Profile, Change Password (dùng chung cho mọi user đã login).
     * `Manager Dashboard` (Màn hình tổng quan của quản lý).
     * `Room Type Management`, `Room Type Details`.
     * `Room Inventory`.
     * `Housekeeping Board`, `Assign Cleaning Tasks` *(UC-51)*.
     * `Maintenance Room List`, `Room Maintenance Details`, `Set Room Maintenance`.
     * `Services Catalog`, `Service Details`.
     * `Discount Voucher Management`, `Voucher Details`.
     * `Review Moderation`, `Review Details`, `Publish Management Reply`.
     * `Reports Dashboard`, `Report Details`, `Export Management Summary`.
     * `Audit Logs` (phần nhật ký vận hành).
   * **Cột `Administrator` (CHỈ giữ `X` ở các mục quản trị kỹ thuật):**
     * `Admin Dashboard`.
     * `User Management`, `User Details`, `Toggle Status`, `Assign Role`.
     * `Audit Configuration` (Cấu hình tham số audit).
     * `Audit Logs`, `Audit Log Details` (Nhật ký bảo mật).
     * *(Bỏ toàn bộ dấu `X` của Administrator ở các màn hình nghiệp vụ phòng, dịch vụ, voucher, báo cáo kinh doanh của Manager).*

---

### 7. Mục 3.6 – Bổ sung đặc tả chi tiết cho UC-51 (Housekeeping Management)
Trong Mục 3.6 của SRS, hiện tại mới chỉ có:
* 3.6.1 & 3.6.2: `UC-19` (Housekeeping Board)
* 3.6.3 đến 3.6.5: `UC-20` (Maintenance)

👉 **Cần bổ sung thêm mục: `3.6.6 UC-51 – Assign Room Cleaning Task`** gồm đầy đủ 4 phần chuẩn:
1. **`3.6.6.1 Mock-up`:**
   * Chèn hình vẽ khung đen trắng (wireframe) màn hình **Gán phòng dọn dẹp**.
   * Các phần tử trên màn hình:
     * `(1)` Tiêu đề màn hình: "GÁN NHIỆM VỤ DỌN PHÒNG (ASSIGN ROOM CLEANING TASK)".
     * `(2)` Bộ lọc phòng trạng thái `Dirty`.
     * `(3)` Bảng danh sách các phòng đang bẩn/khách vừa check-out.
     * `(4)` Dropdown chọn nhân viên buồng phòng (`Housekeeping Staff`) đang trong ca trực.
     * `(5)` Chọn mức độ ưu tiên (Bình thường / Gấp - Priority: Normal / High / Expedited).
     * `(6)` Ô nhập ghi chú / chỉ dẫn đặc biệt (Cleaning Instructions).
     * `(7)` Nút bấm `[XÁC NHẬN GÁN VIỆC - CONFIRM ASSIGNMENT]`.
2. **`Table 3-X: Screen Definition`:**
   * Lập bảng 6 cột chuẩn (`#`, `Field Name`, `Type`, `Mandatory`, `Max Length`, `Description`) mô tả chi tiết các trường `(1)` đến `(7)`.
3. **`3.6.6.2 Use Case Description`:**
   * Bảng Use Case Description 7 cột gộp chuẩn:
     * **Use Case ID:** `UC-51` | **Use Case Name:** `Assign Room Cleaning Task`
     * **Actor:** `Manager`
     * **Precondition:** Hệ thống hoạt động; Manager đã đăng nhập; Có ít nhất 1 phòng có trạng thái `Dirty`; Có nhân viên Housekeeping đang active.
     * **Trigger:** Manager mở màn hình phân công dọn phòng để bố trí nhân sự dọn buồng.
     * **Post-Condition:** Nhiệm vụ dọn buồng được ghi nhận; Phòng hiển thị tên nhân viên phụ trách; Bảng Housekeeping Board của nhân viên đó được cập nhật.
     * **Main Flow:** 4 bước thao tác của Manager và phản hồi của hệ thống.
4. **`Alternative Flows` & `Business Rules`:**
   * **AT1:** Không có nhân viên buồng phòng nào đang active trong ca $\rightarrow$ Hệ thống cảnh báo không thể gán.
   * **AT2:** Phòng đã được người khác gán hoặc đã chuyển trạng thái $\rightarrow$ Hệ thống thông báo làm mới danh sách.

---

### 8. Mục 6.1 – Bảng Quy tắc nghiệp vụ (Table 61: Business Rules)
1. **Sửa quy tắc `BR-06`:**
   * **Cũ:** *"BR-06: Staff roles are Front-Desk Staff, Housekeeping Staff, Service Staff, and Administrator."*
   * **Mới:** *"BR-06: Staff roles are Front-Desk Staff, Housekeeping Staff, Service Staff, **Manager**, and Administrator."*
2. **Bổ sung quy tắc mới cho UC-51:**
   * Thêm **`BR-43`**:
     > *"BR-43: Only rooms with Dirty status can be assigned for housekeeping turnover; cleaning tasks must be assigned to an active Housekeeping Staff member."* (Chỉ những phòng có trạng thái Dirty mới được phép gán nhiệm vụ dọn dẹp; người được gán bắt buộc phải là nhân viên buồng phòng đang có trạng thái Active).

---

## 🚀 TRÌNH TỰ ĐỀ XUẤT ĐỂ NHÓM THỰC HIỆN
1. **Bước 1 (Text & Rules):** Sửa số lượng `51 Use Cases` ở mục 2.2, sửa `BR-06` và thêm `BR-43` ở mục 6.1, sửa `UC-09` trong Table 2.
2. **Bước 2 (Actor Mapping):** Cập nhật toàn bộ các UC quản lý ở Table 2 từ `Administrator` sang `Manager`.
3. **Bước 3 (Table 4 Matrix):** Chèn cột `Manager` vào Bảng 4, thêm dòng `Assign Cleaning Tasks` và tick lại dấu `X`.
4. **Bước 4 (UC-51 Detail):** Viết mục 3.6.6 (Mock-up, Screen Definition, Use Case Description) cho UC-51.
5. **Bước 5 (Diagrams):** Cập nhật các hình vẽ Use Case Diagram (Figure 2-2, Figure 2-5, Figure 1-1) để khớp 100% với tài liệu.
6. **Bước 6 (Review & Log):** Điền vào bảng Record of Changes ở trang đầu và rà soát tính nhất quán.

---
*Tài liệu này được tạo tự động để các thành viên trong nhóm đối chiếu và phân chia công việc nhanh chóng.*
