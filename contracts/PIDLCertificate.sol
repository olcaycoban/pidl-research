// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title PIDLCertificate
 * @notice PIDL Araştırma Platformu — Sepolia Testnet NFT Sertifika Sözleşmesi
 *
 * Katılımcı 12 görevi tamamladığında (6 adaptif + 6 sabit blok) bu sözleşme
 * pseudonim bir ERC-721 NFT sertifikası basar.
 *
 * Pseudonimlik (KVKK): Zincire yalnızca cüzdan adresi + tamamlama hash'i yazılır.
 * Kişisel veri (isim, e-posta) off-chain SQLite/PostgreSQL veritabanında tutulur.
 *
 * Fonksiyonlar:
 *   verifyTask   — Her görev tamamlandığında çağrılır (on-chain log)
 *   mintCertificate — 12 görev bittikten sonra NFT sertifika basar
 *
 * Gas optimizasyonu: uint8 task ID, mapping yerine bitfield kullanımı
 */

interface IERC721 {
    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);
    function balanceOf(address owner) external view returns (uint256);
    function ownerOf(uint256 tokenId) external view returns (address);
}

contract PIDLCertificate is IERC721 {
    // ── State ────────────────────────────────────────────────────────────────
    address public owner;
    uint256 private _nextTokenId = 1;

    // Katılımcı cüzdan adresi → tamamlanan görev bitfield (12 bit)
    mapping(address => uint16) public completedTasks;

    // NFT sahipliği
    mapping(uint256 => address) private _owners;
    mapping(address => uint256) private _balances;

    // Token URI (off-chain IPFS metadata)
    mapping(uint256 => string) private _tokenURIs;

    // Kaç görevin tamamlanması gerekiyor (12 = 6 adaptif + 6 sabit blok)
    uint8 public constant REQUIRED_TASKS = 12;

    // ── Events ───────────────────────────────────────────────────────────────
    event TaskVerified(address indexed student, uint8 taskId, uint256 timestamp);
    event CertificateMinted(address indexed student, uint256 tokenId, uint256 timestamp);

    // ── Modifier ─────────────────────────────────────────────────────────────
    modifier onlyOwner() {
        require(msg.sender == owner, "PIDLCertificate: caller is not owner");
        _;
    }

    // ── Constructor ──────────────────────────────────────────────────────────
    constructor() {
        owner = msg.sender;
    }

    // ── Core Functions ───────────────────────────────────────────────────────

    /**
     * @notice Görev tamamlama kaydı (Oracle olarak PIDL platformu çağırır)
     * @param student Katılımcının Ethereum cüzdan adresi (pseudonim)
     * @param taskId  1-12 arası görev numarası (1-6 adaptif, 7-12 sabit blok)
     */
    function verifyTask(address student, uint8 taskId) external onlyOwner {
        require(student != address(0), "PIDLCertificate: zero address");
        require(taskId >= 1 && taskId <= REQUIRED_TASKS, "PIDLCertificate: invalid taskId");

        uint16 bit = uint16(1) << (taskId - 1);
        completedTasks[student] |= bit;

        emit TaskVerified(student, taskId, block.timestamp);
    }

    /**
     * @notice Tüm görevler tamamlandığında ERC-721 NFT sertifikası bas
     * @param student Katılımcının cüzdan adresi
     * @param metadataURI IPFS metadata URI (sertifika içeriği — kişisel veri YOK)
     */
    function mintCertificate(address student, string calldata metadataURI)
        external
        onlyOwner
        returns (uint256 tokenId)
    {
        require(student != address(0), "PIDLCertificate: zero address");
        require(
            isEligible(student),
            "PIDLCertificate: not all tasks completed"
        );
        require(_balances[student] == 0, "PIDLCertificate: already minted");

        tokenId = _nextTokenId++;
        _owners[tokenId]   = student;
        _balances[student] = 1;
        _tokenURIs[tokenId] = metadataURI;

        emit Transfer(address(0), student, tokenId);
        emit CertificateMinted(student, tokenId, block.timestamp);
    }

    // ── View Functions ───────────────────────────────────────────────────────

    /// @notice Katılımcının tüm 12 görevi tamamlayıp tamamlamadığını döndür
    function isEligible(address student) public view returns (bool) {
        uint16 fullMask = uint16((1 << REQUIRED_TASKS) - 1); // 0b111111111111
        return (completedTasks[student] & fullMask) == fullMask;
    }

    function balanceOf(address addr) external view override returns (uint256) {
        return _balances[addr];
    }

    function ownerOf(uint256 tokenId) external view override returns (address) {
        address addr = _owners[tokenId];
        require(addr != address(0), "PIDLCertificate: token does not exist");
        return addr;
    }

    function tokenURI(uint256 tokenId) external view returns (string memory) {
        require(_owners[tokenId] != address(0), "PIDLCertificate: token does not exist");
        return _tokenURIs[tokenId];
    }

    /// @notice Hangi görevlerin tamamlandığını döndür (uint16 bitfield)
    function getCompletedTasks(address student) external view returns (uint16) {
        return completedTasks[student];
    }

    // ── Owner Utilities ──────────────────────────────────────────────────────

    function transferOwnership(address newOwner) external onlyOwner {
        require(newOwner != address(0), "PIDLCertificate: zero address");
        owner = newOwner;
    }
}
