"""
Persona-aware sentetik prompt ve Solidity kod şablonları (6 görev).

Kullanım:
    from scripts.content_templates import make_prompt, make_code, logical_task_number
"""
from __future__ import annotations

import hashlib
import random
from typing import Tuple

from scripts.humanize_text import humanize

TASK_NAMES = [
    "Diploma Doğrulama",
    "Sertifika NFT",
    "Öğrenme Kaydı",
    "Çoklu İmza",
    "DAO Oylama",
    "Token Teşvik",
]

LEVELS = ["novice", "advanced_beginner", "competent", "proficient", "expert"]
LEVEL_LABELS = {
    "novice": "Acemi",
    "advanced_beginner": "İleri Başlangıç",
    "competent": "Yetkin",
    "proficient": "Usta",
    "expert": "Uzman",
}

TASK_PROMPT_BASE = {
    1: (
        "Lütfen Solidity ^0.8.x ile üniversite diploma doğrulama akıllı sözleşmesi yaz. "
        "Yalnızca owner diploma ekleyebilsin; öğrenci adresi, bytes32 diplomaHash, "
        "isim ve mezuniyet tarihi saklansın. verifyDiploma, revokeDiploma ve isDiplomaValid "
        "fonksiyonları olsun. Reentrancy ve yetkisiz yazma risklerine dikkat et."
    ),
    2: (
        "ERC-721 tabanlı eğitim sertifikası NFT sözleşmesi geliştir. mintCertificate, "
        "tokenURI güncelleme ve sahiplik transferi desteklensin. Sadece sertifika veren "
        "adres mint edebilsin. Metadata IPFS URI formatında tutulsun."
    ),
    3: (
        "Öğrenme ilerlemesini blockchain üzerinde kaydeden bir sözleşme yaz. "
        "recordProgress, getProgress ve tamamlanma yüzdesi hesaplayan view fonksiyonları "
        "ekle. Her öğrenci için modül bazlı skor mapping kullan."
    ),
    4: (
        "2-of-3 çoklu imza cüzdanı Solidity sözleşmesi oluştur. proposeTransaction, "
        "confirmTransaction ve executeTransaction akışı olsun. Eşik değeri ve imzacı "
        "listesi constructor ile ayarlansın."
    ),
    5: (
        "Basit bir DAO oylama sözleşmesi yaz. createProposal, vote ve finalizeProposal "
        "fonksiyonları bulunsun. Oy ağırlığı token bakiyesine bağlı olsun; çift oy "
        "engellensin."
    ),
    6: (
        "Öğrenme teşvik tokenı (ERC-20) sözleşmesi geliştir. completeModule ve claimReward "
        "ile modül tamamlayanlara ödül dağıtılsın. Owner reward havuzunu yönetsin; "
        "pause mekanizması eklensin."
    ),
}


def logical_task_number(task_number: int) -> int:
    """DB task_number 1-12 → görev şablonu 1-6."""
    return ((int(task_number) - 1) % 6) + 1


def _seed(*parts: str) -> int:
    h = hashlib.md5("|".join(parts).encode()).hexdigest()
    return int(h[:8], 16)


def _style_suffix(level: str, mod: str, domain: str) -> str:
    parts = []
    if mod == "Similar":
        parts.append(
            f"Benzer mod: kullanıcının {LEVEL_LABELS.get(level, level)} seviyesine uygun, "
            "adım adım ve anlaşılır bir çıktı üret."
        )
    else:
        parts.append(
            "Tamamlayıcı mod: kullanıcının zayıf olduğu alanları tamamlayacak şekilde "
            "daha derin teknik detay ve ek güvenlik kontrolleri ekle."
        )
    if domain == "educational":
        parts.append(
            "Her önemli satıra Türkçe açıklayıcı yorum ekle; öğrenme hedeflerini "
            "NatSpec @dev ile belirt."
        )
    else:
        parts.append(
            "Gas optimizasyonu, custom error kullanımı ve edge case'leri (sıfır adres, "
            "overflow) ele al."
        )
    return " ".join(parts)


_HUMAN_OPENINGS = [
    "Selam, şu görev için yardıma ihtiyacım var —",
    "Merhaba, biraz karıştım galiba;",
    "Hocam/arkadaşlar, pratikte şöyle bir senaryo düşünüyorum:",
    "Kısaca anlatayım:",
    "Aslında elimde net bir şablon yok ama",
]

_HUMAN_MIDDLES = [
    "benzer şekilde ilerlemek istiyorum,",
    "biraz acelem var ama mantığını da anlamak istiyorum,",
    "yani hem çalışsın hem de neden böyle yazdığımı göreyim,",
    "sanırım temel iskelet yeterli olur, detayı sonra düşünürüz,",
]

_HUMAN_CLOSINGS = [
    "Tek dosyada çalışır bir örnek yeterli, teşekkürler.",
    "Mümkünse tek Solidity dosyasında toparlar mısın?",
    "Kodu kopyalayıp deneyeceğim; yorum satırları işime yarar.",
    "Hata mesajlarını da Türkçe/İngilizce kısa tutarsan sevinirim.",
]


def make_prompt(
    task_number: int,
    level: str,
    mod: str,
    domain: str,
    *,
    seed: int | None = None,
) -> str:
    """50–120 kelime, konuşma diline yakın görev promptu."""
    tn = logical_task_number(task_number)
    base = TASK_PROMPT_BASE[tn]
    style = _style_suffix(level, mod, domain)
    extras = {
        1: "Örnek olarak İstanbul Üniversitesi mezunları için doğrulama düşünüyorum.",
        2: "Kurs bitince benzersiz tokenId üretsin istiyorum.",
        3: "5 modüllük bir program var, her modül 0–100 puan gibi.",
        4: "Eğitim kurumu, denetçi ve öğrenci temsilcisi imzacı olsun.",
        5: "Müfredat güncelleme için 7 günlük oylama senaryosu.",
        6: "Modül başına mesela 10 PITL token ödülü verilebilir.",
    }
    rng = random.Random(seed if seed is not None else _seed(str(tn), level, mod, domain))
    opening = rng.choice(_HUMAN_OPENINGS)
    middle = rng.choice(_HUMAN_MIDDLES)
    closing = rng.choice(_HUMAN_CLOSINGS)
    task_label = TASK_NAMES[tn - 1]

    # Uzun tek cümle + kısa ekler → netlik skoru her zaman 100 olmaz
    prompt = (
        f"{opening} {task_label} konusunda {middle} {base} "
        f"{extras[tn]} {style} {closing}"
    )
    if rng.random() > 0.55:
        prompt += " OpenZeppelin Ownable falan kullanılabilir belki."
    if mod == "Complementary" and rng.random() > 0.35:
        prompt += " Bir de yorum satırında kısa test senaryosu yazarsan iyi olur."
    if domain == "educational" and rng.random() > 0.5:
        prompt += " Öğrenirken takıldığım yerler için @dev notu ekle lütfen."
    # Bazen ikinci paragraf (daha insansı, biraz dağınık)
    if rng.random() > 0.65:
        prompt += (
            f"\n\nEk not: {LEVEL_LABELS.get(level, level)} seviyesindeyim, "
            "çok akademik anlatma; pratik örnek yeter."
        )
    hseed = (seed if seed is not None else _seed(str(tn), level, mod, domain)) + 17
    return humanize(prompt, random.Random(hseed), intensity=rng.uniform(0.9, 1.0))


def _tier(quality_score: float) -> str:
    if quality_score < 55:
        return "low"
    if quality_score < 75:
        return "mid"
    return "high"


def _code_diploma(tier: str, domain: str) -> str:
    if tier == "low":
        return """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DiplomaRegistry {
    address public owner;
    mapping(address => bytes32) public diplomas;

    constructor() { owner = msg.sender; }

    function addDiploma(address student, bytes32 hash) public {
        require(msg.sender == owner);
        diplomas[student] = hash;
    }

    function verifyDiploma(address student) public view returns (bytes32) {
        return diplomas[student];
    }
}
"""
    if tier == "mid":
        return """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DiplomaRegistry {
    address public owner;
    struct Diploma {
        bytes32 diplomaHash;
        string studentName;
        uint256 graduationDate;
        bool revoked;
    }
    mapping(address => Diploma) public records;

    constructor() { owner = msg.sender; }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    function addDiploma(
        address student,
        bytes32 diplomaHash,
        string memory studentName,
        uint256 graduationDate
    ) external onlyOwner {
        require(student != address(0));
        records[student] = Diploma(diplomaHash, studentName, graduationDate, false);
    }

    function verifyDiploma(address student)
        external
        view
        returns (bool valid, bytes32 hash, string memory name, uint256 date)
    {
        Diploma memory d = records[student];
        valid = d.diplomaHash != bytes32(0) && !d.revoked;
        return (valid, d.diplomaHash, d.studentName, d.graduationDate);
    }

    function revokeDiploma(address student) external onlyOwner {
        records[student].revoked = true;
    }

    function isDiplomaValid(address student) external view returns (bool) {
        Diploma memory d = records[student];
        return d.diplomaHash != bytes32(0) && !d.revoked;
    }
}
"""
    ped = """
    /// @dev Öğrenci kaydı: hash değiştirilemez referans içerir
""" if domain == "educational" else ""
    return f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title Diploma Doğrulama — üniversite kayıt defteri
contract DiplomaRegistry {{
    address public immutable admin;
    struct Diploma {{
        bytes32 diplomaHash;
        string studentName;
        uint256 graduationDate;
        bool revoked;
    }}
    mapping(address => Diploma) private _records;
    event DiplomaIssued(address indexed student, bytes32 hash);
    event DiplomaRevoked(address indexed student);

    error Unauthorized();
    error InvalidStudent();

    constructor() {{ admin = msg.sender; }}

    modifier onlyAdmin() {{
        if (msg.sender != admin) revert Unauthorized();
        _;
    }}
{ped}
    function addDiploma(
        address student,
        bytes32 diplomaHash,
        string calldata studentName,
        uint256 graduationDate
    ) external onlyAdmin {{
        if (student == address(0)) revert InvalidStudent();
        _records[student] = Diploma(diplomaHash, studentName, graduationDate, false);
        emit DiplomaIssued(student, diplomaHash);
    }}

    function verifyDiploma(address student)
        external
        view
        returns (bool valid, bytes32 hash, string memory name, uint256 date)
    {{
        Diploma memory d = _records[student];
        valid = d.diplomaHash != bytes32(0) && !d.revoked;
        return (valid, d.diplomaHash, d.studentName, d.graduationDate);
    }}

    function revokeDiploma(address student) external onlyAdmin {{
        _records[student].revoked = true;
        emit DiplomaRevoked(student);
    }}

    function isDiplomaValid(address student) external view returns (bool) {{
        Diploma memory d = _records[student];
        return d.diplomaHash != bytes32(0) && !d.revoked;
    }}
}}
"""


def _code_nft(tier: str, domain: str) -> str:
    if tier == "low":
        return """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CertificateNFT {
    mapping(uint256 => address) public ownerOf;
    uint256 public nextId;

    function mint(address to) public {
        ownerOf[nextId] = to;
        nextId++;
    }
}
"""
    if tier == "mid":
        return """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CertificateNFT {
    address public minter;
    mapping(uint256 => address) private _owners;
    mapping(uint256 => string) private _uris;
    uint256 public tokenCounter;

    constructor() { minter = msg.sender; }

    function mintCertificate(address to, string memory uri) external {
        require(msg.sender == minter);
        uint256 id = tokenCounter++;
        _owners[id] = to;
        _uris[id] = uri;
    }

    function tokenURI(uint256 id) external view returns (string memory) {
        return _uris[id];
    }
}
"""
    return """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CertificateNFT {
    address public issuer;
    mapping(uint256 => address) private _owners;
    mapping(uint256 => string) private _tokenURIs;
    uint256 private _nextTokenId;

    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);

    error NotIssuer();
    error InvalidRecipient();

    constructor() { issuer = msg.sender; }

    modifier onlyIssuer() {
        if (msg.sender != issuer) revert NotIssuer();
        _;
    }

    function mintCertificate(address to, string calldata uri) external onlyIssuer returns (uint256) {
        if (to == address(0)) revert InvalidRecipient();
        uint256 tokenId = _nextTokenId++;
        _owners[tokenId] = to;
        _tokenURIs[tokenId] = uri;
        emit Transfer(address(0), to, tokenId);
        return tokenId;
    }

    function tokenURI(uint256 tokenId) external view returns (string memory) {
        return _tokenURIs[tokenId];
    }
}
"""


def _code_learning(tier: str, domain: str) -> str:
    if tier == "low":
        return """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract LearningLog {
    mapping(address => uint256) public scores;

    function recordProgress(address student, uint256 score) public {
        scores[student] = score;
    }

    function getProgress(address student) public view returns (uint256) {
        return scores[student];
    }
}
"""
    if tier == "mid":
        return """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract LearningLog {
    mapping(address => mapping(uint256 => uint256)) public moduleScores;
    uint256 public moduleCount = 5;

    function recordProgress(address student, uint256 moduleId, uint256 score) external {
        require(moduleId < moduleCount);
        require(score <= 100);
        moduleScores[student][moduleId] = score;
    }

    function getProgress(address student, uint256 moduleId) external view returns (uint256) {
        return moduleScores[student][moduleId];
    }

    function completionPercent(address student) external view returns (uint256) {
        uint256 sum;
        for (uint256 i = 0; i < moduleCount; i++) {
            sum += moduleScores[student][i];
        }
        return sum / moduleCount;
    }
}
"""
    return """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract LearningLog {
    uint256 public constant MODULE_COUNT = 5;
    mapping(address => mapping(uint256 => uint256)) private _scores;
    event ProgressRecorded(address indexed student, uint256 moduleId, uint256 score);

    function recordProgress(address student, uint256 moduleId, uint256 score) external {
        require(moduleId < MODULE_COUNT, "Invalid module");
        require(score <= 100, "Score cap");
        _scores[student][moduleId] = score;
        emit ProgressRecorded(student, moduleId, score);
    }

    function getProgress(address student, uint256 moduleId) external view returns (uint256) {
        return _scores[student][moduleId];
    }

    function completionPercent(address student) external view returns (uint256) {
        uint256 total;
        for (uint256 i = 0; i < MODULE_COUNT; i++) {
            total += _scores[student][i];
        }
        return total / MODULE_COUNT;
    }
}
"""


def _code_multisig(tier: str, domain: str) -> str:
    if tier == "low":
        return """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MultiSig {
    address[] public signers;
    uint256 public required;

    constructor(address[] memory _signers, uint256 _required) {
        signers = _signers;
        required = _required;
    }

    function execute(address target, uint256 value, bytes memory data) public {
        (bool ok,) = target.call{value: value}(data);
        require(ok);
    }
}
"""
    if tier == "mid":
        return """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MultiSigWallet {
    address[] public owners;
    uint256 public required;
    struct Transaction {
        address to;
        uint256 value;
        bytes data;
        bool executed;
        uint256 confirmations;
    }
    Transaction[] public txs;
    mapping(uint256 => mapping(address => bool)) public confirmed;

    constructor(address[] memory _owners, uint256 _required) {
        require(_required > 0 && _required <= _owners.length);
        owners = _owners;
        required = _required;
    }

    function proposeTransaction(address to, uint256 value, bytes memory data) external returns (uint256) {
        txs.push(Transaction(to, value, data, false, 0));
        return txs.length - 1;
    }

    function confirmTransaction(uint256 txId) external {
        confirmed[txId][msg.sender] = true;
        txs[txId].confirmations++;
    }
}
"""
    return """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MultiSigWallet {
  address[] public owners;
  uint256 public immutable threshold;
  struct Tx { address to; uint256 value; bytes data; bool executed; uint256 confirmations; }
  Tx[] private _queue;
  mapping(uint256 => mapping(address => bool)) private _confirmed;

  event Submission(uint256 indexed txId);
  event Execution(uint256 indexed txId);

  constructor(address[] memory _owners, uint256 _threshold) {
    require(_threshold > 0 && _threshold <= _owners.length);
    owners = _owners;
    threshold = _threshold;
  }

  function proposeTransaction(address to, uint256 value, bytes calldata data) external returns (uint256 txId) {
    _queue.push(Tx(to, value, data, false, 0));
    txId = _queue.length - 1;
    emit Submission(txId);
  }

  function confirmTransaction(uint256 txId) external {
    require(!_confirmed[txId][msg.sender]);
    _confirmed[txId][msg.sender] = true;
    _queue[txId].confirmations++;
  }

  function executeTransaction(uint256 txId) external {
    Tx storage t = _queue[txId];
    require(!t.executed && t.confirmations >= threshold);
    t.executed = true;
    (bool ok,) = t.to.call{value: t.value}(t.data);
    require(ok);
    emit Execution(txId);
  }
}
"""


def _code_dao(tier: str, domain: str) -> str:
    if tier == "low":
        return """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SimpleDAO {
    mapping(uint256 => uint256) public votesFor;
    mapping(uint256 => mapping(address => bool)) public voted;

    function vote(uint256 proposalId) external {
        require(!voted[proposalId][msg.sender]);
        voted[proposalId][msg.sender] = true;
        votesFor[proposalId]++;
    }
}
"""
    if tier == "mid":
        return """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SimpleDAO {
    struct Proposal {
        string description;
        uint256 deadline;
        uint256 yesVotes;
        uint256 noVotes;
        bool finalized;
    }
    Proposal[] public proposals;
    mapping(uint256 => mapping(address => bool)) public hasVoted;

    function createProposal(string memory description, uint256 duration) external returns (uint256) {
        proposals.push(Proposal(description, block.timestamp + duration, 0, 0, false));
        return proposals.length - 1;
    }

    function vote(uint256 proposalId, bool support) external {
        require(!hasVoted[proposalId][msg.sender]);
        require(block.timestamp < proposals[proposalId].deadline);
        hasVoted[proposalId][msg.sender] = true;
        if (support) proposals[proposalId].yesVotes++;
        else proposals[proposalId].noVotes++;
    }
}
"""
    return """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SimpleDAO {
  struct Proposal {
    string description;
    uint256 deadline;
    uint256 yesVotes;
    uint256 noVotes;
    bool finalized;
  }
  Proposal[] private _proposals;
  mapping(uint256 => mapping(address => bool)) private _voted;

  event ProposalCreated(uint256 indexed id);
  event Voted(uint256 indexed id, address indexed voter, bool support);

  function createProposal(string calldata description, uint256 duration) external returns (uint256 id) {
    _proposals.push(Proposal(description, block.timestamp + duration, 0, 0, false));
    id = _proposals.length - 1;
    emit ProposalCreated(id);
  }

  function vote(uint256 proposalId, bool support) external {
    Proposal storage p = _proposals[proposalId];
    require(!_voted[proposalId][msg.sender] && block.timestamp < p.deadline);
    _voted[proposalId][msg.sender] = true;
    if (support) p.yesVotes++; else p.noVotes++;
    emit Voted(proposalId, msg.sender, support);
  }

  function finalizeProposal(uint256 proposalId) external {
    Proposal storage p = _proposals[proposalId];
    require(block.timestamp >= p.deadline && !p.finalized);
    p.finalized = true;
  }
}
"""


def _code_token(tier: str, domain: str) -> str:
    if tier == "low":
        return """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract RewardToken {
    mapping(address => uint256) public balances;
    uint256 public totalSupply;

    function mint(address to, uint256 amount) public {
        balances[to] += amount;
        totalSupply += amount;
    }
}
"""
    if tier == "mid":
        return """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract RewardToken {
    address public owner;
    mapping(address => uint256) public balances;
    mapping(address => mapping(uint256 => bool)) public moduleCompleted;

    constructor() { owner = msg.sender; }

    function completeModule(address student, uint256 moduleId) external {
        moduleCompleted[student][moduleId] = true;
    }

    function claimReward(address student, uint256 moduleId) external {
        require(moduleCompleted[student][moduleId]);
        moduleCompleted[student][moduleId] = false;
        balances[student] += 10 ether;
    }
}
"""
    return """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract RewardToken {
  address public owner;
  bool public paused;
  mapping(address => uint256) public balances;
  mapping(address => mapping(uint256 => bool)) private _completed;

  event RewardClaimed(address indexed student, uint256 moduleId, uint256 amount);

  modifier onlyOwner() { require(msg.sender == owner); _; }
  modifier whenNotPaused() { require(!paused); _; }

  constructor() { owner = msg.sender; }

  function completeModule(address student, uint256 moduleId) external onlyOwner {
    _completed[student][moduleId] = true;
  }

  function claimReward(address student, uint256 moduleId) external whenNotPaused {
    require(_completed[student][moduleId]);
    _completed[student][moduleId] = false;
    uint256 reward = 10 ether;
    balances[student] += reward;
    emit RewardClaimed(student, moduleId, reward);
  }

  function pause() external onlyOwner { paused = true; }
  function unpause() external onlyOwner { paused = false; }
}
"""


_CODE_BUILDERS = {
    1: _code_diploma,
    2: _code_nft,
    3: _code_learning,
    4: _code_multisig,
    5: _code_dao,
    6: _code_token,
}


def make_code(
    task_number: int,
    level: str,
    mod: str,
    domain: str,
    quality_score: float,
    *,
    seed: int | None = None,
) -> str:
    """Kalite skoruna göre kademeli Solidity kodu."""
    tn = logical_task_number(task_number)
    tier = _tier(quality_score)
    code = _CODE_BUILDERS[tn](tier, domain)
    rng = random.Random(seed if seed is not None else _seed("code", str(tn), level, mod, domain))
    if domain == "educational" and tier == "high" and "// @dev" not in code:
        code = code.replace(
            "pragma solidity",
            "// @dev Bu sözleşme eğitim amaçlı örnek implementasyondur\npragma solidity",
            1,
        )
    if mod == "Complementary" and tier != "low" and rng.random() > 0.6:
        code += "\n// Tamamlayıcı mod: ek güvenlik incelemesi önerilir.\n"
    return code


def make_content(
    task_number: int,
    level: str,
    mod: str,
    domain: str,
    quality_score: float,
    duration_minutes: float,
) -> Tuple[str, str, float]:
    """(prompt, code, generation_time_seconds)"""
    seed = _seed(str(task_number), level, mod, domain, str(int(quality_score)))
    prompt = make_prompt(task_number, level, mod, domain, seed=seed)
    code = make_code(task_number, level, mod, domain, quality_score, seed=seed + 1)
    gen_sec = round(max(8.0, duration_minutes * 60 * 0.15 + (seed % 40)), 1)
    return prompt, code, gen_sec
