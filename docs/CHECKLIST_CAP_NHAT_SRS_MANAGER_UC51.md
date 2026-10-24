# KẾ HOẠCH CẬP NHẬT TÀI LIỆU ĐẶC TẢ YÊU CẦU PHẦN MỀM (SRS)
## DỰ ÁN: HOTEL MANAGEMENT SYSTEM (HMS)
**Tài liệu áp dụng:** `HMS_SoftwareRequirementSpecification-4.docx`  
**Ngày cập nhật trạng thái:** 24/10/2026  
**Mục tiêu chỉnh sửa:** 
1. Tách vai trò `Administrator` thành 2 vai trò: **`Administrator`** (Quản trị viên kỹ thuật IT) và **`Manager`** (Quản lý nghiệp vụ khách sạn).
2. Bổ sung **`UC-51: Assign Room Cleaning Task`** (Gán phòng dọn dẹp cho nhân viên buồng phòng) vào Subsystem 2.

---

## 📌 BẢNG TỔNG HỢP TIẾN ĐỘ THỰC HIỆN

| STT | Vị trí trong SRS | Hạng mục công việc | Chi tiết đã làm / Cần làm | Phụ trách | Trạng thái |
|:---:|:---|:---|:---|:---:|:---:|
| **1** | **Bìa & Mục I** | Record of Changes (Table 0) | Đã thêm dòng lịch sử phiên bản ngày 24/10 chi tiết | AI / Trưởng nhóm | ✅ **ĐÃ XONG** |
| **2** | **Mục 2.2** | Tổng số Use Case & Mô tả Subsystem | Đã sửa từ 50 thành 51 UCs; cập nhật Subsystem 2 gồm 11 UCs (UC11–UC20, UC-51) | AI / Nhóm | ✅ **ĐÃ XONG** |
| **3** | **Mục 2.2.2** | Table 2 (Use Case Descriptions) | Đã chuyển Actor sang `Manager` ở 18 UCs quản lý; cập nhật `UC-09` thêm role Manager; kiểm tra `UC-51` | AI / Nhóm | ✅ **ĐÃ XONG** |
| **4** | **Mục 3.1.3** | Table 4 (Screen Authorization Matrix) | Đã cấu trúc lại ma trận 9 cột: thêm cột `Manager`, thêm hàng `UC-51` và `Manager Dashboard`, phân quyền chuẩn | AI / Nhóm | ✅ **ĐÃ XONG** |
| **5** | **Mục 3.6.6** | Đặc tả chi tiết chức năng UC-51 | Đã tạo Mockup giao diện kèm số callout, Table 3-22 Screen Definition, Use Case Description, Alternative Flows | AI / Nhóm | ✅ **ĐÃ XONG** |
| **6** | **Mục 6.1** | Business Rules (Table 65) | Đã cập nhật **BR-06** thêm `Manager`; đã thêm quy tắc mới **BR-43** cho việc gán dọn phòng Dirty | AI / Nhóm | ✅ **ĐÃ XONG** |
| **7** | **Mục 1.2** | Context Diagram (Figure 1-1) | Vẽ lại sơ đồ ngữ cảnh bổ sung Actor `Manager` | Thành viên nhóm (Design) | ⏳ **CẦN LÀM** |
| **8** | **Mục 2.2.1** | Subsystem 1 UC Diagram (Figure 2-1) | Cập nhật Administrator chỉ nối tới UC-07, 08, 09 | Thành viên nhóm (Design) | ⏳ **CẦN LÀM** |
| **9** | **Mục 2.2.1** | Subsystem 2 UC Diagram (Figure 2-2) | Thêm Manager, nối UC-51, chuyển UC 11–17 sang Manager | Thành viên nhóm (Design) | ⏳ **CẦN LÀM** |
| **10** | **Mục 2.2.1** | Subsystem 4 UC Diagram (Figure 2-4) | Chuyển UC-31, 32, 33 sang Actor Manager | Thành viên nhóm (Design) | ⏳ **CẦN LÀM** |
| **11** | **Mục 2.2.1** | Subsystem 5 UC Diagram (Figure 2-5) | Chuyển UC-43, 44, 45, 46, 47, 50 sang Manager; Audit log nối cả 2 | Thành viên nhóm (Design) | ⏳ **CẦN LÀM** |
| **12** | **Toàn tài liệu** | Chèn ảnh Diagram mới & Update Mục lục | Dán 5 ảnh diagram mới vào docx; bấm F9 cập nhật Table of Contents | Cả nhóm | ⏳ **CẦN LÀM** |

---

## 🟢 PHẦN A: CÁC NỘI DUNG ĐÃ HOÀN THÀNH TRONG FILE DOCX
*(Đã được cập nhật tự động trực tiếp vào file `docs/HMS_SoftwareRequirementSpecification-4.docx`)*

### 1. Mục I – Record of Changes (Table 0)
- Đã thêm dòng ghi nhận thay đổi vào cuối bảng:
  - **Date:** `24/10/2026`
  - **A, M, D:** `M, A`
  - **Description:** Tách vai trò Administrator thành Administrator (Quản trị hệ thống) và Manager (Quản lý nghiệp vụ); Bổ sung UC-51 Assign Room Cleaning Task vào Subsystem 2; Cập nhật ma trận phân quyền Table 4 (9 cột), Use Case Descriptions (Table 2), Business Rules BR-06/BR-43 và đặc tả Section 3.6.6.

### 2. Mục 2.2 – Tổng số Use Cases & Mô tả Subsystem
- Đã sửa câu mở đầu: *"The system provides **51 use cases** partitioned into five functional subsystems:"*
- Đã sửa mô tả Subsystem 2: *"Subsystem 2: Room & Facility Management **(UC11 – UC20, UC-51)**: Covers room category configuration, inventory setup, room browsing, housekeeping workflow, **cleaning task assignment**, and maintenance tracking."* (11 Use Cases).

### 3. Mục 2.2.2 – Table 2 (Use Case Descriptions)
- Đã rà soát và chuyển cột Actor sang **`Manager`** tại tất cả các Use Case nghiệp vụ:
  - `UC-11`, `UC-12`, `UC-13` (Room Type Management)
  - `UC-14` (View Room Categories) $\rightarrow$ `Customer, Front-Desk Staff, Manager`
  - `UC-15`, `UC-16`, `UC-17` (Room Inventory Setup & Archive)
  - `UC-18` (View Room Inventory) $\rightarrow$ `Front-Desk Staff, Housekeeping Staff, Manager`
  - `UC-20` (Set Room Maintenance) $\rightarrow$ `Housekeeping Staff, Manager`
  - `UC-31`, `UC-32`, `UC-33` (Service Management & Tariffs)
  - `UC-43` (Publish Management Reply) $\rightarrow$ `Front-Desk Staff, Manager`
  - `UC-44` (Moderate Review Visibility)
  - `UC-45`, `UC-46`, `UC-47` (Báo cáo kinh doanh, công suất, doanh thu, dịch vụ)
  - `UC-49` (Inspect Audit Logs) $\rightarrow$ `Manager, Administrator`
  - `UC-50` (Export Management Dashboard Summary)
- Đã cập nhật bước 2 của **`UC-09 (Assign User Roles)`**: Bổ sung `Manager` vào danh sách vai trò cấp phát: *(Front-Desk Staff, Housekeeping Staff, Service Staff, **Manager**, Administrator)*.
- Giữ nguyên thông tin của `UC-51 (Assign Room Cleaning Task)` với Actor là `Manager`.

### 4. Mục 3.1.3 – Table 4 (Screen Authorization Matrix)
- Đã thay thế bảng phân quyền cũ thành bảng **9 cột hoàn chỉnh chuẩn xác**:
  - `[#, Screen / Function, Guest / Public, Customer, Front-Desk Staff, Housekeeping Staff, Service Staff, Manager, Administrator]`
- Đã thêm dòng:
  - `17.3: Assign Cleaning Tasks (UC-51)` $\rightarrow$ Chỉ cấp quyền cho **`Manager`**.
  - `21: Manager Dashboard` $\rightarrow$ Chỉ cấp quyền cho **`Manager`**.
- Đã rút gọn quyền của `Administrator` chỉ tập trung vào: User Accounts, Toggle Status, Assign Role, Admin Dashboard, Audit Configuration, và Security Audit Logs. Toàn bộ các màn hình kinh doanh khách sạn đã chuyển sang `Manager`.

### 5. Mục 3.6.6 – Đặc tả chi tiết chức năng UC-51
- Đã viết mới toàn bộ Section 3.6.6 đặt ngay trước Section 4:
  - **3.6.6.1 Mock-up:** Chèn hình ảnh giao diện phân công dọn buồng (`fig_3_22_assign_cleaning.png`) có đánh số callout đỏ `(1)` đến `(7)`.
  - **Table 3-22: Screen Definition:** Bảng 6 cột chuẩn quy định các trường: Tiêu đề, Bộ lọc phòng Dirty, Bảng phòng bẩn chờ dọn, Dropdown nhân viên buồng phòng trực ca, Chọn mức độ ưu tiên, Chỉ dẫn dọn dẹp, Nút xác nhận gán việc.
  - **3.6.6.2 Use Case Description:** Bảng 7 cột gộp chuẩn (Actor: Manager, Preconditions, Triggers, Post-conditions, Main Flow 4 bước).
  - **Alternative Flows:** `AT1` (Không có nhân viên dọn buồng active), `AT2` (Phòng đã thay đổi trạng thái hoặc đã được gán trước).
  - **Business Rules:** Tham chiếu áp dụng `BR-43` và `BR-06`.

### 6. Mục 6.1 – Business Rules (Bảng 65)
- Đã cập nhật **`BR-06`**: Bổ sung `Manager` vào danh sách vai trò nhân viên.
- Đã thêm quy tắc mới **`BR-43`**:
  > *"BR-43: Only rooms with Dirty status can be assigned for housekeeping turnover; cleaning tasks must be assigned to an active Housekeeping Staff member."*

---

## 🔴 PHẦN B: CÁC CÔNG VIỆC CẦN LÀM DÀNH CHO CÁC THÀNH VIÊN TRONG NHÓM
*(Do các thành viên phụ trách vẽ diagram bằng Draw.io / StarUML / Visio thực hiện)*

### 1. Vẽ lại Figure 1-1: Context Diagram (Sơ đồ ngữ cảnh hệ thống)
* **Vị trí trong tài liệu:** Mục 1.2 (trang ~12).
* **Nội dung cần sửa trên hình:**
  * Bổ sung Actor box **`Manager`** bên cạnh các actor hiện tại.
  * Đường nối tương tác: `Manager` gửi các yêu cầu thiết lập phòng, giá dịch vụ, xem báo cáo, gán phòng dọn dẹp $\rightarrow$ Hệ thống HMS phản hồi dữ liệu tổng hợp.
  * Phân biệt rõ: `Administrator` chỉ tương tác với module quản trị tài khoản và cấu hình hệ thống IT.

### 2. Vẽ lại Figure 2-1: Subsystem 1 Use Case Diagram (Account & Auth)
* **Vị trí trong tài liệu:** Mục 2.2.1 (Subsystem 1).
* **Nội dung cần sửa trên hình:**
  * Đảm bảo Actor **`Administrator`** chỉ kết nối tới 3 Use Cases kỹ thuật:
    - `UC-07: Manage User Accounts`
    - `UC-08: Toggle User Account Status`
    - `UC-09: Assign User Roles`
  * (Các actor khác giữ nguyên: Guest, Customer, Front-Desk, Housekeeping, Service Staff).

### 3. Vẽ lại Figure 2-2: Subsystem 2 Use Case Diagram (Room & Facility Management)
* **Vị trí trong tài liệu:** Mục 2.2.1 (Subsystem 2).
* **Nội dung quan trọng nhất:**
  * **Thêm Actor `Manager`** vào diagram.
  * Thêm bong bóng Use Case: **`UC-51: Assign Room Cleaning Task`** và nối Actor `Manager` $\rightarrow$ `UC-51`.
  * **Chuyển toàn bộ các Use Case quản lý phòng sang Actor `Manager`:**
    - `UC-11: Create Room Type`
    - `UC-12: Update Room Type Details`
    - `UC-13: Deactivate Room Category`
    - `UC-15: Create Room`
    - `UC-16: Update Room Details`
    - `UC-17: Archive Room`
  * `UC-14 (View Room Categories)`: Nối tới Customer, Front-Desk Staff, Manager.
  * `UC-18 (View Room Inventory)`: Nối tới Front-Desk Staff, Housekeeping Staff, Manager.
  * `UC-19 (Manage Housekeeping Status)`: Nối tới Housekeeping Staff.
  * `UC-20 (Set Room Maintenance)`: Nối tới Housekeeping Staff, Manager.
  * *(Xóa Actor Administrator ra khỏi biểu đồ Subsystem 2 vì Admin không quản lý phòng).*

### 4. Vẽ lại Figure 2-4: Subsystem 4 Use Case Diagram (Ancillary Services)
* **Vị trí trong tài liệu:** Mục 2.2.1 (Subsystem 4).
* **Nội dung cần sửa trên hình:**
  * Chuyển các đường nối của nhóm quản lý bảng giá dịch vụ sang Actor **`Manager`**:
    - `UC-31: Create Hotel Service`
    - `UC-32: Update Service Tariff`
    - `UC-33: Deactivate Hotel Service`
  * *(Xóa Actor Administrator ra khỏi Figure 2-4).*

### 5. Vẽ lại Figure 2-5: Subsystem 5 Use Case Diagram (Reviews, Audit & Reporting)
* **Vị trí trong tài liệu:** Mục 2.2.1 (Subsystem 5).
* **Nội dung cần sửa trên hình:**
  * **Thêm Actor `Manager`**: Nối tới các chức năng nghiệp vụ quản lý:
    - `UC-43: Publish Management Reply` (Nối chung với Front-Desk)
    - `UC-44: Moderate Review Visibility`
    - `UC-45: Generate Room Occupancy Report`
    - `UC-46: Generate Revenue Analytics Report`
    - `UC-47: Analyze Service Consumption`
    - `UC-50: Export Management Dashboard Summary`
  * **`UC-49: Inspect System Audit Logs`**: Nối cả 2 Actor **`Manager`** và **`Administrator`** (Manager xem Operational Audit Logs, Administrator xem Security Audit Logs).
  * **`UC-48: Configure Audit Parameters`**: Chỉ nối với **`Administrator`**.

---

## 🛠️ HƯỚNG DẪN HOÀN TẤT & XUẤT BẢN FILE CUỐI CÙNG

Khi các thành viên trong nhóm vẽ xong 5 hình diagram trên (định dạng `.png` rõ nét):
1. **Chèn ảnh vào Word:** Mở file `docs/HMS_SoftwareRequirementSpecification-4.docx`, chuột phải vào các hình cũ (Figure 1-1, 2-1, 2-2, 2-4, 2-5) $\rightarrow$ chọn **Change Picture (Đổi ảnh)** $\rightarrow$ chọn file ảnh mới vẽ. Cách này giúp giữ nguyên caption và định dạng của Word.
2. **Cập nhật Mục lục (Update Fields):**
   - Nhấn `Ctrl + A` (hoặc `Cmd + A` trên Mac) để chọn toàn bộ văn bản.
   - Nhấn phím **`F9`** (hoặc chuột phải vào mục lục $\rightarrow$ chọn *Update Field* $\rightarrow$ *Update entire table*).
   - Word sẽ tự động cập nhật số trang cho Table of Contents, List of Tables và List of Figures khớp 100%.
3. **Lưu và xuất PDF:** Lưu file Word và Export ra file `.pdf` nộp cho giảng viên.
